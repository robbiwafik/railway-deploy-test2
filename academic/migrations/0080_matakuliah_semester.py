# Generated by Django 4.2.2 on 2023-07-17 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0079_rename_jumlah_pratikum_matakuliah_jumlah_sks_praktik_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='matakuliah',
            name='semester',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]
