from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
from django.contrib import admin
from django.db.models import Q, F
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth import get_user_model
from import_export.admin import ImportExportModelAdmin

from . import models
from . import forms
from . import mixins

@admin.register(models.Kurikulum)
class KurikulumAdmin(admin.ModelAdmin):
    list_display = ['kode', 'nama', 'tanggal_digunakan']


@admin.register(models.UptTIK)
class UptTIKAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']

    def isUptTIKUser(self, request):
        return hasattr(request.user, 'upttik')
    
    def get_queryset(self, request):
        if hasattr(request.user, 'upttik'):
            return models.UptTIK.objects.filter(user_id=request.user.id)
        return super().get_queryset(request)
    
    def has_add_permission(self, request):
        if self.isUptTIKUser(request):
            return False
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=models.UptTIK):
        if self.isUptTIKUser(request):
            return False
        return super().has_delete_permission(request, obj)
    
    def changelist_view(self, request, extra_context=None):
        if self.isUptTIKUser(request):
            upttik = self.get_queryset(request).first()
            app_name = self.model._meta.app_label
            model_name = self.model._meta.model_name
            url = reverse(f'admin:{app_name}_{model_name}_change', args=[upttik.id])
            return HttpResponseRedirect(url)
        return super().changelist_view(request, extra_context)
    

@admin.register(models.Jurusan)
class JurusanAdmin(admin.ModelAdmin):
    list_display = ['id', 'nama']
    ordering = ['id']


@admin.register(models.Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['no']
    ordering = ['no']


@admin.register(models.ProgramPendidikan)
class ProgramPendidikanAdmin(admin.ModelAdmin):
    list_display = ['kode', 'nama']


@admin.register(models.GedungKuliah)
class GedungKuliahAdmin(admin.ModelAdmin):
    list_display = ['id', 'nama']
    ordering = ['id']


class FilterJurusanInline(admin.TabularInline):
    extra = 0
    model = models.PemberitahuanJurusan
    verbose_name = ''
    verbose_name_plural = 'Filter'


class FilterProdiInline(admin.TabularInline):
    extra = 0
    model = models.PemberitahuanProdi
    verbose_name = ''
    verbose_name_plural = 'Filter'


@admin.register(models.Pemberitahuan)
class PemberitahuanAdmin(admin.ModelAdmin):
    fields = ['judul', 'sub_judul', 'detail', 'tanggal_hapus', 'file', 'link', 'thumbnail', 'preview']
    list_display = ['id', 'judul', 'tanggal_terbit', 'tanggal_hapus']
    list_per_page = 10
    ordering = ['-tanggal_terbit']
    readonly_fields = ['preview']
    search_fields = ['judul']

    def isStaffProdi(self, request):
        return hasattr(request.user, 'staffprodi')

    def preview(self, pemberitahuan):
        if pemberitahuan.thumbnail:
            return format_html(f"<img class='thumbnail' src='/media/{pemberitahuan.thumbnail}' />")
        return None
    
    def get_queryset(self, request):
        if self.isStaffProdi(request):
            return models.Pemberitahuan.objects.filter(
                Q(filter_prodi__prodi=request.user.staffprodi.prodi) | Q(filter_prodi__isnull=True)
            )
            
        return super().get_queryset(request)
    
    def get_inline_instances(self, request, obj=None):
        if self.isStaffProdi(request):
            return []
        return [FilterJurusanInline(self.model, self.admin_site), 
                FilterProdiInline(self.model, self.admin_site)]
            
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        pemberitahuan_prodi = models.PemberitahuanProdi.objects.filter(pemberitahuan_id=obj.id).first()
        if not pemberitahuan_prodi and self.isStaffProdi(request):
            models.PemberitahuanProdi.objects.create(
                pemberitahuan_id=obj.id,
                prodi=request.user.staffprodi.prodi
            )
            
            
    class Media:
        css = {
            'all': ['academic/styles.css']
        }


@admin.register(models.ProgramStudi)
class ProgramStudiAdmin(admin.ModelAdmin):
    list_display = ['kode', 'nama', 'tanggal_sk', 
                    'tahun_operasional', 'jurusan']
    search_fields = ['nama']

    def changelist_view(self, request, extra_context=None):
        if hasattr(request.user, 'staffprodi'):
            prodi = request.user.staffprodi.prodi
            app_name = self.model._meta.app_label
            model_name = self.model._meta.model_name
            url = reverse(f'admin:{app_name}_{model_name}_change', args=[prodi.id])
            return HttpResponseRedirect(url)
        return super().changelist_view(request, extra_context)
    
    class Media:
        css = {
            'all': ['academic/program_studi_styles.css']
        }

@admin.register(models.StaffProdi)
class StaffProdiAdmin(admin.ModelAdmin):
    autocomplete_fields = ['prodi', 'user']
    list_display = ['no_induk', 'nama', 'email', 'username']
    list_per_page = 10
    list_select_related = ['user']
    search_fields = ['user__first_name']

    def nama(self, staff_prodi):
        return f'{staff_prodi.user.first_name} {staff_prodi.user.last_name}'
    
    def changelist_view(self, request, extra_context=None):
        if hasattr(request.user, 'staffprodi'):
            app_name = self.model._meta.app_label
            model_name = self.model._meta.model_name
            url = reverse(f'admin:{app_name}_{model_name}_change', args=[request.user.staffprodi.id])
            return HttpResponseRedirect(url)
        return super().changelist_view(request, extra_context)
 

@admin.register(models.Dosen)
class DosenAdmin(admin.ModelAdmin):
    autocomplete_fields = ['prodi', 'user']
    list_display = ['nip', 'nama', 'no_hp', 'gelar', 'prodi']
    list_per_page = 10
    readonly_fields = ['preview']
    search_fields = ['nama']

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': True,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': False
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

    def preview(self, dosen):
        if dosen.foto_profil:
            return format_html(f'<img class="thumbnail" src="/media/{dosen.foto_profil}" />')
        return None

    def get_queryset(self, request):
        if hasattr(request.user, 'staffprodi'):
            return models.Dosen.objects.filter(prodi=request.user.staffprodi.prodi)
        return super().get_queryset(request)
        
    def changelist_view(self, request: HttpRequest, extra_context: Dict[str, str] | None = ...) -> TemplateResponse:
        if hasattr(request.user, 'dosen'):
            app_name = self.model._meta.app_label
            model_name = self.model._meta.model_name
            url = reverse(f'admin:{app_name}_{model_name}_change', args=[request.user.dosen.id])
            return HttpResponseRedirect(url)
        return super().changelist_view(request, extra_context)

    def get_fields(self, request: HttpRequest, obj: Any | None = ...) -> Sequence[Callable[..., Any] | str]:
        fields = super().get_fields(request, obj)
        if hasattr(request.user, 'dosen'):
            fields.remove('user')
        return fields
        
        

    class Media:
        css = {
            'all': ['academic/styles.css']
        }


@admin.register(models.Kelas)
class KelasAdmin(admin.ModelAdmin):
    autocomplete_fields = ['prodi']
    list_display = ['id', 'prodi', 'semester', 'huruf', 'nama_kurikulum', 'mahasiswa']
    list_per_page = 10
    ordering = ['semester', 'huruf']
    search_fields = ['prodi']
    radio_fields = {'semester': admin.VERTICAL}

    def mahasiswa(self, kelas):
        query_str = f'?kelas_id={kelas.id}'
        url = reverse(f'admin:academic_mahasiswa_changelist') + query_str
        return format_html(f'<a class="btn-link" href="{url}">Mahasiswa</a>')
        
    def get_queryset(self, request):
        if hasattr(request.user, 'staffprodi'):
            return models.Kelas.objects.filter(prodi=request.user.staffprodi.prodi)
        return super().get_queryset(request)

    class Media:
        css = {
            "all": ["academic/styles.css"]
        }


class MahasiswaFilter(admin.SimpleListFilter):
    title = 'semester'
    parameter_name = 'semester'

    def lookups(self, request, model_admin):
         return [(semester.no, f'Semester {semester.no}') for semester in list(models.Semester.objects.all())]
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(kelas__semester=self.value())
        return queryset.all()


@admin.register(models.Mahasiswa)
class MahasiswaAdmin(admin.ModelAdmin):
    autocomplete_fields = ['pembimbing_akademik', 'user']
    fields = ['nim', 'tanggal_lahir', 'no_hp', 'alamat', 
              'tahun_angkatan', 'pembimbing_akademik', 'kelas',
              'user', 'foto_profil', 'preview']
    list_display = ['nim', 'nama', 'username', 'kelas']
    list_filter = [MahasiswaFilter]
    list_per_page = 10
    search_fields = ['nama']
    readonly_fields = ['preview']

    def preview(self, mahasiswa):
        if mahasiswa.foto_profil:
            return format_html(f'<img class="thumbnail" src="/media/{mahasiswa.foto_profil}" />')
        return None

    def nama(self, mahasiswa):
        return f'{mahasiswa.user.first_name} {mahasiswa.user.last_name}'

    def username(self, mahasiswa):
        return mahasiswa.user.username

    def get_queryset(self, request):
        if hasattr(request.user, 'staffprodi'):
            prodi = request.user.staffprodi.prodi
            return models.Mahasiswa.objects.filter(kelas__prodi=prodi)
        elif hasattr(request.user, 'dosen'):
            dosen = request.user.dosen
            jadwal_dosen = list(models.JadwalMakul.objects.filter(dosen=dosen))
            jadwal_dosen_kelas_id = [jadwal_makul.jadwal.kelas.id for jadwal_makul in jadwal_dosen]
            return models.Mahasiswa.objects.filter(kelas_id__in=jadwal_dosen_kelas_id)
        return super().get_queryset(request)

    class Media:
        css = {
            'all': ['academic/styles.css']
        }


@admin.register(models.Ruangan)
class RuanganAdmin(admin.ModelAdmin):
    list_display = ['id', 'nama', 'gedung']
    list_filter = ['gedung']
    search_fields = ['nama']
    list_per_page = 10

    def aduan(self, ruangan):
        query_str = f"?ruangan_id={ruangan.id}"
        url = reverse('admin:academic_aduanruangan_changelist') + query_str
        return format_html(f'<a class="btn-link" href="{url}">Aduan</a>')
    
    def get_list_display(self, request: HttpRequest) -> Sequence[str]:
        list_display = super().get_list_display(request)
        if hasattr(request.user, 'upttik'):
            list_display.append('aduan')
        return list_display

    class Media:
        css = {
            'all': ['academic/styles.css']
        }
    

@admin.register(models.AduanRuangan)
class AduanRuanganAdmin(admin.ModelAdmin):
    list_display = ['id', 'detail', 'ruangan', 'status']
    list_per_page = 10
    readonly_fields = ['detail', 'ruangan', 'foto', 'preview', 'mahasiswa']
    search_fields = ['detail']
    radio_fields = {'status': admin.HORIZONTAL}

    def preview(self, aduan_ruangan):
        if aduan_ruangan.foto:
            return format_html(f'<img style="width: 500px; height: 500px;" class="bigger-edthumbnail" src="/media/{aduan_ruangan.foto}" />')
        return None

    class Media:
        css = {
            'all': ['academic/styles.css']
        }


@admin.register(models.KaryaIlmiah)
class KaryaIlmiahAdmin(admin.ModelAdmin):
    list_display = ['judul', 'tanggal_terbit', 'tipe', 'prodi']
    search_fields = ['judul', 'mahasiswa__nim']
    list_filter = ['tipe']
    list_per_page = 10
    autocomplete_fields = ['mahasiswa', 'prodi']
    exclude = ['prodi']

    def get_queryset(self, request):
        if hasattr(request.user, 'staffprodi'):
            return models.KaryaIlmiah.objects.filter(prodi=request.user.staffprodi.prodi)
        elif hasattr(request.user, 'dosen'):
            return models.KaryaIlmiah.objects.filter(prodi=request.user.dosen.prodi)
        return super().get_queryset(request)
    

    def get_fields(self, request: HttpRequest, obj: Any | None = ...) -> Sequence[Callable[..., Any] | str]:
        fields = super().get_fields(request, obj)
        print(fields)
        if hasattr(request.user, 'dosen'):
            fields.remove('mahasiswa')
        return fields
    

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        if (obj.mahasiswa):
            obj.prodi = obj.mahasiswa.kelas.prodi
        elif hasattr(request.user, 'dosen'):
            obj.prodi = request.user.dosen.prodi
        
        return obj.save()
    

class MataKuliahInline(admin.TabularInline):
    model = models.JadwalMakul
    extra = 0
    fields = ['mata_kuliah', 'ruangan', 'dosen',
              'hari', 'jam_mulai', 'jam_selesai']
    autocomplete_fields = ['mata_kuliah', 'ruangan', 'dosen']
    

@admin.register(models.Jadwal)
class JadwalAdmin(admin.ModelAdmin):
    autocomplete_fields = ['kelas']
    inlines = [MataKuliahInline]
    list_display = ['id', 'kelas', 'nama_kurikulum']
    list_per_page = 10
    ordering = ['kelas']

    def get_queryset(self, request):
        if hasattr(request.user, 'staffprodi'):
            prodi = request.user.staffprodi.prodi
            return models.Jadwal.objects.filter(kelas__prodi=prodi)
        return super().get_queryset(request)


class SemesterTypeFilter(admin.SimpleListFilter):
    title = 'Tipe Semester'
    parameter_name = 'semester_type'

    def lookups(self, request: Any, model_admin: Any) -> List[Tuple[Any, str]]:
        return [
            ('odd', 'Ganjil'),
            ('even', 'Genap')
        ]
    
    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == 'odd':
            return queryset.annotate(odd=F('semester') % 2).filter(odd=True)
        elif self.value() == 'even':
            return queryset.annotate(odd=F('semester') % 2).filter(odd=False)
        return queryset
        

@admin.register(models.MataKuliah)
class MataKuliahAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    exclude = ['program_studi']
    list_display = ['kode', 'nama', 'jumlah_sks_teori', 
                    'jumlah_sks_praktik', 'semester', 'nama_kurikulum']
    list_filter = ['semester', SemesterTypeFilter]
    search_fields = ['nama']
    list_per_page = 15

    def has_import_permission(self, request):
        if hasattr(request.user, 'dosen'):
            return False
        return super().has_import_permission(request)
    
    def has_export_permission(self, request):
        
        return super().has_export_permission(request)

    def get_queryset(self, request):
        if hasattr(request.user, 'staffprodi'):
            prodi = request.user.staffprodi.prodi
            return models.MataKuliah.objects.filter(program_studi=prodi)
        elif hasattr(request.user, 'dosen'):
            dosen = request.user.dosen
            jadwal_makul_dosen = models.JadwalMakul.objects.filter(dosen_id=dosen.id)
            makul_dosen_id = [jadwal_makul.mata_kuliah.id for jadwal_makul in jadwal_makul_dosen]
            return models.MataKuliah.objects.filter(id__in=set(makul_dosen_id))
        return super().get_queryset(request)
    
    def save_model(self, request, obj, form, change):
        if hasattr(request.user, 'staffprodi'):
            obj.program_studi = request.user.staffprodi.prodi
        obj.save()


@admin.register(models.NilaiKHS)
class NilaiKHSAdmin(admin.ModelAdmin):
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        if hasattr(request.user, 'dosen'):
            dosen = request.user.dosen
            jadwal_makul_dosen = models.JadwalMakul.objects.filter(dosen_id=dosen.id)
            makul_dosen_id = [jadwal_makul.mata_kuliah.id for jadwal_makul in jadwal_makul_dosen]
            return models.NilaiKHS.objects.filter(mata_kuliah_id__in=set(makul_dosen_id))
        return super().get_queryset(request)


class NilaiKHSInline(admin.TabularInline):
    autocomplete_fields = ['mata_kuliah']
    extra = 0
    fields = ['mata_kuliah', 'nilai']
    model = models.NilaiKHS
    verbose_name_plural = 'Nilai KHS'
    formset = forms.NilaiKHSInlineFormset

    def get_formset(self, request: Any, obj: Any | None = ..., **kwargs: Any) -> Any:
        formset = super(NilaiKHSInline, self).get_formset(request, obj, **kwargs)
        formset.request = request
        return formset


@admin.register(models.KHS)
class KHSAdmin(admin.ModelAdmin):
    autocomplete_fields = ['mahasiswa']
    fields = ['mahasiswa', 'tahun_akademik_awal', 'tahun_akademik_akhir', 'semester']
    inlines = [NilaiKHSInline]
    list_display = ['mahasiswa', 'semester', 'tahun_akademik', 'kelas']
    list_filter = ['semester', 'kelas']
    search_fields = ['mahasiswa__nim', 'tahun_akademik_awal', 'tahun_akademik_akhir']
    change_form_template = "khs_change_form.html"

    def response_change(self, request: HttpRequest, khs: Any) -> HttpResponse:
        if "cetak_khs" in request.POST:
            return HttpResponseRedirect(f'/academic/generate_pdf?model=khs&khs_id={khs.id}')
        return super().response_change(request, khs)

    def tahun_akademik(self, khs):
        return f"{khs.tahun_akademik_awal}/{khs.tahun_akademik_akhir}"
    
    def get_queryset(self, request):
        if hasattr(request.user, 'staffprodi'):
            prodi = request.user.staffprodi.prodi
            return models.KHS.objects.filter(mahasiswa__kelas__prodi=prodi)
        return super().get_queryset(request)

    def save_model(self, request, obj, form, change):
        obj.program_studi = str(obj.mahasiswa.kelas.prodi.nama)
        obj.program_pendidikan = str(obj.mahasiswa.kelas.prodi.program_pendidikan.nama)
        obj.dosen_pembimbing = str(obj.mahasiswa.pembimbing_akademik.nama)
        obj.kelas = str(obj.mahasiswa.kelas.huruf)
        obj.save()


@admin.register(models.KetuaJurusan)
class KetuaJurusanAdmin(admin.ModelAdmin):
    list_display = ['id', 'nama', 'gelar']


@admin.register(models.KoordinatorProgramStudi)
class KoordinatorProgramStudiAdmin(admin.ModelAdmin):
    list_display = ['id', 'nama', 'gelar']


@admin.register(models.JadwalMakul)
class JadwalMakulAdmin(admin.ModelAdmin):
    search_fields = ['kelas__prodi, kelas__semester, mata_kuliah__nama']

    def get_search_results(self, request: HttpRequest, queryset: QuerySet[Any], search_term: str) -> Tuple[QuerySet[Any], bool]:
        queryset, may_have_duplicates = super().get_search_results(request, queryset, search_term)
        if hasattr(request.user, 'dosen'):
            queryset = queryset.filter(dosen_id=request.user.dosen.id)
        return queryset, may_have_duplicates

class JadwalMakulFilter(admin.SimpleListFilter):
    title = 'Kelas'
    parameter_name = 'kelas'

    def lookups(self, request: Any, model_admin: Any) -> List[Tuple[Any, str]]:
        if hasattr(request.user, 'dosen'):
            jadwal_makul_list = list(models.JadwalMakul.objects.filter(dosen=request.user.dosen))
            return [
                (jadwal_makul.id, f'{jadwal_makul.jadwal.kelas.prodi} {jadwal_makul.jadwal.kelas.semester} {jadwal_makul.jadwal.kelas.huruf} {jadwal_makul.mata_kuliah.nama}') \
                for jadwal_makul in jadwal_makul_list
            ]
        return super().lookups(request, model_admin)
    
    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        queryset = models.Materi.objects.all()
        if (self.value()):
            return queryset.filter(jadwal_makul_id=self.value())
        return queryset


@admin.register(models.Materi)
class MateriAdmin(admin.ModelAdmin):
    #The field 'jadwal_makul' in this model is changed to 'kelas' to prevent confusion of 'Dosen' actor

    autocomplete_fields = ['jadwal_makul']
    list_display = ['judul', 'kelas']
    list_filter = [JadwalMakulFilter]

    def get_form(self, request: Any, obj: Any | None = ..., change: bool = ..., **kwargs: Any) -> Any:
        form = super().get_form(request, obj, change, **kwargs)
        form.base_fields['jadwal_makul'].label = 'Kelas'
        return form
    


        