from rest_framework import serializers

from . import models


class JurusanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Jurusan
        fields = ['id', 'nama']


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Semester
        fields = ['no']


class ProgramPendidikanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProgramPendidikan
        fields = ['kode', 'nama']


class GedungKuliahSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GedungKuliah
        fields = ['id', 'nama']


class PemberitahuanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pemberitahuan
        fields = ['id', 'judul', 'sub_judul', 
                  'detail', 'tanggal_terbit', 'tanggal_hapus', 
                  'thumbnail', 'file', 'link']


class ProgramStudiSerializer(serializers.ModelSerializer):
    jurusan = JurusanSerializer()
    program_pendidikan = ProgramPendidikanSerializer()
    class Meta:
        model = models.ProgramStudi
        fields = ['kode', 'nama', 'no_sk', 
                  'tanggal_sk', 'tahun_operasional', 'jurusan', 
                  'program_pendidikan', 'akreditasi']


class SimpleProgramStudiSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProgramStudi
        fields = ['id', 'kode', 'nama']


class CreateUpdateProgramStudiSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProgramStudi
        fields = ['kode', 'nama', 'no_sk', 
                  'tanggal_sk', 'tahun_operasional', 'jurusan', 
                  'program_pendidikan']


class StaffProdiSerializer(serializers.ModelSerializer):
    prodi = SimpleProgramStudiSerializer()
    class Meta:
        model = models.StaffProdi
        fields = ['no_induk', 'nama_depan', 'nama_belakang', 'username', 'email', 'no_hp', 'prodi']


class CreateUpdateStaffProdiSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StaffProdi
        fields = ['no_induk', 'no_hp', 'prodi', 'user']


class SimpleMataKuliahSerializer(serializers.ModelSerializer):
    sks = serializers.SerializerMethodField()

    def get_sks(self, mata_kuliah:models.MataKuliah):
        return mata_kuliah.jumlah_sks_teori + mata_kuliah.jumlah_sks_praktik
        
    class Meta:
        model = models.MataKuliah
        fields = ['kode', 'nama', 'sks']


class SimpleKelasSerializer(serializers.ModelSerializer):
    prodi = SimpleProgramStudiSerializer()
    class Meta:
        model = models.Kelas
        fields = ['id', 'prodi', 'semester', 'huruf']


class SimpleJadwalSerializer(serializers.ModelSerializer):
    semester = serializers.SerializerMethodField()

    def get_semester(self, jadwal):
        return jadwal.kelas.semester.no

    class Meta:
        model = models.Jadwal
        fields = ['id', 'semester']


class DosenJadwalMakulSerializer(serializers.ModelSerializer):
    jadwal = SimpleJadwalSerializer()
    mata_kuliah = SimpleMataKuliahSerializer()
    nama_hari = serializers.CharField(source='get_hari_display',  read_only=True)
    ruangan = serializers.SerializerMethodField()

    def get_ruangan(self, jadwalMakul: models.JadwalMakul):
        return {'nama': jadwalMakul.ruangan.nama, 'gedung': jadwalMakul.ruangan.gedung.nama}

    class Meta:
        model = models.JadwalMakul
        fields = ['id', 'jam_mulai', 'jam_selesai', 'nama_hari', 'ruangan', 'mata_kuliah', 'jadwal']


class DosenSerializer(serializers.ModelSerializer):
    prodi = SimpleProgramStudiSerializer()
    makul_ajar = DosenJadwalMakulSerializer(many=True)
    
    class Meta:
        model = models.Dosen
        fields = ['nip', 'nama', 'email', 'no_hp', 'gelar', 'prodi', 'foto_profil', 'makul_ajar']


class SimpleDosenSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dosen
        fields = ['nip', 'nama', 'gelar']


class CreateUpdateDosenSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dosen
        fields = ['nip', 'nama', 'email', 'no_hp', 'gelar', 'prodi']


class KelasSerializer(serializers.ModelSerializer):
    prodi = ProgramStudiSerializer()
    class Meta:
        model = models.Kelas
        fields = ['id', 'huruf', 'prodi', 'semester']


class CreateUpdateKelasSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Kelas
        fields = ['id', 'prodi', 'semester', 'huruf']


class MahasiswaSerializer(serializers.ModelSerializer):
    kelas = KelasSerializer()
    pembimbing_akademik = SimpleDosenSerializer()

    class Meta:
        model = models.Mahasiswa
        fields = ['nim', 'nama_depan', 'nama_belakang', 'username',
                  'email', 'tahun_angkatan', 'tanggal_lahir', 'alamat', 
                  'no_hp', 'foto_profil', 'pembimbing_akademik', 
                  'kelas']


class SimpleMahasiswaSerializer(serializers.ModelSerializer):
    nama = serializers.SerializerMethodField(method_name='get_nama')

    def get_nama(self, mahasiswa: models.Mahasiswa):
        return f"{mahasiswa.user.first_name} {mahasiswa.user.last_name}"
    
    class Meta:
        model = models.Mahasiswa
        fields = ['nim', 'nama', 'foto_profil']


class CreateUpdateMahasiswaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Mahasiswa
        fields = ['tanggal_lahir', 'tahun_angkatan',
                  'alamat', 'no_hp', 'foto_profil', 
                  'pembimbing_akademik', 'kelas', 'user']


class AduanRuanganSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AduanRuangan
        fields = ['id', 'status', 'detail', 'foto', 'ruangan', 'tanggapan', 'mahasiswa']


class CreateAduanRuanganSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return models.AduanRuangan.objects.create(ruangan_id=self.context['ruangan_id'], **validated_data)
    
    class Meta:
        model = models.AduanRuangan
        fields = ['id', 'detail', 'foto']


class UpdateAduanRuanganSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AduanRuangan
        fields = ['status']


class PemberitahuanProdiSerializer(serializers.ModelSerializer):
    prodi = SimpleProgramStudiSerializer()
    
    class Meta:
        model = models.PemberitahuanProdi
        fields = ['id', 'prodi']


class CreatePemberitahuanProdiSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return models.PemberitahuanProdi.objects.create(
            pemberitahuan_id=self.context['pemberitahuan_id'],
            **validated_data
        )
    
    class Meta:
        model = models.PemberitahuanProdi
        fields = ['id', 'prodi']


class PemberitahuanJurusanSerializer(serializers.ModelSerializer):
    jurusan = JurusanSerializer()
    
    class Meta:
        model = models.PemberitahuanJurusan
        fields = ['id', 'jurusan']


class SimplePemberitahuanSerializer(serializers.ModelSerializer):
    filter_prodi = PemberitahuanProdiSerializer(many=True)
    filter_jurusan = PemberitahuanJurusanSerializer(many=True)
    
    class Meta:
        model = models.Pemberitahuan
        fields = ['id', 'judul', 'sub_judul', 
                  'thumbnail', 'filter_prodi', 'filter_jurusan']


class CreatePemberitahuanJurusanSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return models.PemberitahuanJurusan.objects.create(
            pemberitahuan_id=self.context['pemberitahuan_id'],
            **validated_data
        )

    class Meta:
        model = models.PemberitahuanJurusan
        fields = ['id', 'jurusan']


class KaryaIlmiahSerializer(serializers.ModelSerializer):
    mahasiswa = SimpleMahasiswaSerializer()
    prodi = SimpleProgramStudiSerializer()
    kode_tipe = serializers.CharField(source='tipe')
    tipe = serializers.CharField(source='get_tipe_display', read_only=True)

    class Meta:
        model = models.KaryaIlmiah
        fields = ['id', 'judul', 'abstrak', 
                  'tanggal_terbit', 'link_versi_full', 'kode_tipe',
                  'file_preview', 'prodi', 'mahasiswa', 'tipe']


class CreateUpdateKaryaIlmiahSerializer(serializers.ModelSerializer):
    nim = serializers.CharField(write_only=True)

    def create(self, validated_data):
        nim = validated_data.pop('nim')
        validated_data['mahasiswa'] = models.Mahasiswa.objects.filter(nim=nim).first()
        validated_data['prodi'] = validated_data['mahasiswa'].kelas.prodi

        return super().create(validated_data)

    class Meta:
        model = models.KaryaIlmiah
        fields = ['id', 'judul', 'abstrak',
                  'link_versi_full', 'tipe', 'file_preview', 
                  'nim']


class MataKuliahSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MataKuliah
        fields = ['kode', 'nama', 'jumlah_sks_teori', 
                  'jumlah_sks_praktik']


class SimpleJadwalMakulSerializer(serializers.ModelSerializer):
    kelas = serializers.SerializerMethodField()
    nama_hari = serializers.CharField(source='get_hari_display',  read_only=True)
    mata_kuliah = SimpleMataKuliahSerializer()
    dosen = SimpleDosenSerializer()

    def get_kelas(self, jadwal_makul:models.JadwalMakul):
        serializer = SimpleKelasSerializer(jadwal_makul.jadwal.kelas)
        return serializer.data
    
    class Meta:
        model = models.JadwalMakul
        fields = ['id', 'nama_hari', 'jam_mulai', 'jam_selesai', 'dosen', 'mata_kuliah', 'kelas']


class CreateUpdateJadwalMakulSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return models.JadwalMakul.objects.create(
            jadwal_id=self.context['jadwal_id'],
            **validated_data
        )
    
    class Meta:
        model = models.JadwalMakul
        fields = ['id', 'hari', 'jam_mulai'
                  'jam_selesai', 'dosen', 'ruangan', 
                  'mata_kuliah']
        

class RuanganSerializer(serializers.ModelSerializer):
    jadwal_pemakaian = SimpleJadwalMakulSerializer(many=True, source='jadwalmakul_set', read_only=True)
    gedung = GedungKuliahSerializer()
    
    class Meta:
        model = models.Ruangan
        fields = ['id', 'nama', 'gedung', 'jadwal_pemakaian']


class SimpleRuanganSerializer(serializers.ModelSerializer):
    gedung = GedungKuliahSerializer()
    class Meta:
        model = models.Ruangan
        fields = ['id', 'nama', 'gedung']


class JadwalMakulSerializer(serializers.ModelSerializer):
    kode_hari = serializers.CharField(source='hari')
    hari = serializers.CharField(source='get_hari_display',  read_only=True)
    dosen = SimpleDosenSerializer()
    ruangan = SimpleRuanganSerializer()
    mata_kuliah = SimpleMataKuliahSerializer()
    nama_hari = serializers.CharField(source='get_hari_display',  read_only=True)
    
    class Meta:
        model = models.JadwalMakul
        fields = ['id', 'hari', 'kode_hari', 'jam_mulai', 'nama_hari',
                  'jam_selesai', 'dosen', 'ruangan', 'mata_kuliah', 'materi_set']    


class JadwalSerializer(serializers.ModelSerializer):
    kelas = SimpleKelasSerializer()
    makul_list = JadwalMakulSerializer(many=True)
    
    class Meta:
        model = models.Jadwal
        fields = ['id', 'kelas', 'makul_list']


class CreateUpdateJadwalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Jadwal
        fields = ['id', 'kelas']


class NilaiKHSSerializer(serializers.ModelSerializer):
    mata_kuliah = SimpleMataKuliahSerializer()
    class Meta:
        model = models.NilaiKHS
        fields = ['id', 'mata_kuliah', 'angka_mutu', 'huruf_mutu',
                  'nilai', 'khs']


class CreateUpdateNilaiKHSSerializer(serializers.ModelSerializer):
    def get_huruf_mutu(self, nilai):
        if nilai in range(0, 50):
            return 'E'
        elif nilai in range(50, 60):
            return 'D'
        elif nilai in range(60, 70):
            return 'C'
        elif nilai in range(70, 80):
            return 'B'
        return 'A'

    def get_angka_mutu(self, huruf_mutu):
        if huruf_mutu == 'E':
            return 0
        elif huruf_mutu == 'D':
            return 1
        elif huruf_mutu == 'C':
            return 2
        elif huruf_mutu == 'B':
            return 3
        return 4
    
    def create(self, validated_data):
        khs_id = self.context['khs_id']
        nilai = validated_data['nilai']
        huruf_mutu = self.get_huruf_mutu(nilai)
        angka_mutu = self.get_angka_mutu(huruf_mutu)
        return models.NilaiKHS.objects.create(
            khs_id=khs_id,
            huruf_mutu=huruf_mutu,
            angka_mutu=angka_mutu,
            **validated_data
        )
    
    def update(self, instance, validated_data):
        nilai = validated_data['nilai']
        validated_data['huruf_mutu'] = self.get_huruf_mutu(nilai)
        validated_data['angka_mutu'] = self.get_angka_mutu(validated_data['huruf_mutu'])
        return super().update(instance, validated_data)
    
    class Meta:
        model = models.NilaiKHS
        fields = ['id', 'mata_kuliah', 'nilai']


class KHSSerializer(serializers.ModelSerializer):
    mahasiswa = SimpleMahasiswaSerializer()
    tahun_akademik = serializers.SerializerMethodField()
    nilai_list = NilaiKHSSerializer(many=True)
    ips = serializers.SerializerMethodField('calculate_ips')

    def get_tahun_akademik(self, khs: models.KHS):
        return f'{khs.tahun_akademik_awal} / {khs.tahun_akademik_akhir}'
    
    def calculate_ips(self, khs: models.KHS):
        sum_angka_mutu = 0
        count_angka_mutu = 0
        for nilai in khs.nilai_list.all():
            count_angka_mutu += 1
            sum_angka_mutu += nilai.angka_mutu

        return round(sum_angka_mutu / count_angka_mutu, 2)

    class Meta:
        model = models.KHS
        fields = ['id', 'semester', 'mahasiswa', 'kelas', 
                  'dosen_pembimbing', 'nilai_list', 'program_studi', 
                  'program_pendidikan', 'tahun_akademik', 'ips']


class CreateKHSSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        nim = self.validated_data['mahasiswa']
        mahasiswa = models.Mahasiswa\
            .objects.select_related('kelas', 'kelas__prodi', 'kelas__prodi__program_pendidikan', 
                                    'kelas__semester', 'pembimbing_akademik')\
            .filter(nim=nim).first()
        
        return models.KHS.objects.create(
            semester=mahasiswa.kelas.semester.no,
            program_studi=mahasiswa.kelas.prodi.nama,
            program_pendidikan=mahasiswa.kelas.prodi.program_pendidikan.nama,
            dosen_pembimbing=f"{mahasiswa.pembimbing_akademik.nama} {mahasiswa.pembimbing_akademik.gelar}",
            kelas = mahasiswa.kelas.huruf,
            **self.validated_data
        )
                
    class Meta:
        model = models.KHS
        fields = ['id', 'mahasiswa', 'tahun_akademik_awal',
                  'tahun_akademik_akhir']


class MateriSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Materi
        fields = ['id', 'judul', 'deskripsi', 'tanggal_unggah', 'file', 'jadwal_makul']