from datetime import datetime
from django.shortcuts import render

from . import models

months_in_bahasa = {
    '1': 'Januari',
    '2': 'Februari',
    '3': 'Maret',
    '4': 'April',
    '5': 'Mei',
    '6': 'Juni',
    '7': 'Juli',
    '8': 'Agustus',
    '9': 'September',
    '10': 'Oktober',
    '11': 'November',
    '12': 'Desember'
}

def print_khs(request, khs_id):
    khs = models.KHS.objects.filter(pk=khs_id).first()
    ketua_jurusan = models.KetuaJurusan.objects.filter(jurusan__id=khs.mahasiswa.kelas.prodi.jurusan.id).first()
    koordinator_prodi = models.KoordinatorProgramStudi.objects.filter(program_studi__nama=khs.program_studi).first()
    khs_scores = [score for score in khs.nilai_list.all()]
    sks_total = 0
    total_score = 0
    quality_value_total = 0
    for score in khs_scores:
        sks = score.mata_kuliah.jumlah_sks_teori + score.mata_kuliah.jumlah_sks_praktik
        sks_total += sks
        total_score += score.angka_mutu
        quality_value_total += (score.angka_mutu * sks)
    
    ips = round(total_score / len(khs_scores), 2)
    status = 'LULUS' if ips > 2 else 'TIDAK LULUS'
    today = datetime.today()
    today_date = f'{today.day} {months_in_bahasa[str(today.month)]} {today.year}'

    context = {
        'khs_scores': khs_scores,
        'sks_total': sks_total,
        'tahun_akademik': f'{khs.tahun_akademik_awal}/{khs.tahun_akademik_akhir}',
        'nilai_mutu_total': quality_value_total,
        'ips': ips,
        'mahasiswa': khs.mahasiswa,
        'kelas': khs.kelas,
        'semester': khs.semester,
        'program_studi': khs.program_studi,
        'program_pendidikan': khs.program_pendidikan,
        'status': status,
        'today_date': today_date,
        'ketua_jurusan': ketua_jurusan,
        'koordinator_prodi': koordinator_prodi
    }

    return render(request, 'khs.html', context)

