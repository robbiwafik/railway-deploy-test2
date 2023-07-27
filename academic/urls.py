from django.urls import path, include
from rest_framework_nested import routers

from . import views

router = routers.SimpleRouter()
router.register('dosen', views.DosenViewSet, basename='dosen')
router.register('gedung', views.GedungKuliahViewSet, basename='gedung')
router.register('jurusan', views.JurusanViewSet, basename='jurusan')
router.register('karya_ilmiah', views.KaryaIlmiahViewSet, basename='karya_ilmiah')
router.register('kelas', views.KelasViewSet, basename='kelas')
router.register('mahasiswa', views.MahasiswaViewSet, basename='mahasiswa')
router.register('makul', views.MataKuliahViewSet, basename='makul')
router.register('prodi', views.ProgramStudiViewSet, basename='prodi')
router.register('program_pendidikan', views.ProgramPendidikanViewSet, basename='program_pendidikan')
router.register('semester', views.SemesterViewSet, basename='semester')
router.register('staff_prodi', views.StaffProdiViewSet, basename='staff_prodi')
router.register('materi', views.MateriViewSet, basename='materi')

router.register('ruangan', views.RuanganViewSet, basename='ruangan')
ruangan_aduan = routers.NestedSimpleRouter(router, 'ruangan', lookup='ruangan')
ruangan_aduan.register('aduan', views.AduanRuanganViewSet, basename='ruangan-aduan')

router.register('pemberitahuan', views.PemberitahuanViewSet, basename='pemberitahuan')
pemberitahuan_prodi = routers.NestedDefaultRouter(router, 'pemberitahuan', lookup='pemberitahuan')
pemberitahuan_prodi.register('prodi', views.PemberitahuanProdiViewSet, basename='pemberitahuan-prodi')
pemberitahuan_jurusan = routers.NestedDefaultRouter(router, 'pemberitahuan', lookup='pemberitahuan')
pemberitahuan_jurusan.register('jurusan', views.PemberitahuanJurusanViewSet, basename='pemberitahuan-jurusan')

router.register('jadwal', views.JadwalViewSet, basename='jadwal')
jadwal_makul = routers.NestedDefaultRouter(router, 'jadwal', lookup='jadwal')
jadwal_makul.register('makul', views.JadwalMakulViewSet, basename='jadwal-makul')

router.register('khs', views.KHSViewSet, basename='khs')
nilai_khs = routers.NestedDefaultRouter(router, 'khs', lookup='khs')
nilai_khs.register('nilai', views.NilaiKHSViewSet, basename='nilai')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(ruangan_aduan.urls)),
    path('', include(pemberitahuan_prodi.urls)),
    path('', include(pemberitahuan_jurusan.urls)),
    path('', include(jadwal_makul.urls)),
    path('', include(nilai_khs.urls)),
    path('generate_pdf', views.GeneratePdf.as_view())
]
