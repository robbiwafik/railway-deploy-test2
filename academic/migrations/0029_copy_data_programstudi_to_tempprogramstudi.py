# Generated by Django 4.1.7 on 2023-03-13 02:38

from django.db import migrations, connection


def copy_data(apps, schema_editor):
    with connection.cursor() as cursor:
        cursor.execute('''
            INSERT INTO academic_tempprogramstudi 
                (kode, nama, jurusan_id, program_pendidikan_id, no_sk, tanggal_sk, tahun_operasional)
            SELECT
                kode, nama, jurusan_id, program_pendidikan_id, '-' AS no_sk, '2008-07-08' AS tanggal_sk, 2008 AS tahun_operasional
            FROM academic_programstudi;
            '''
        )

class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0028_tempprogramstudi'),
    ]

    operations = [
        migrations.RunPython(copy_data)
    ]

