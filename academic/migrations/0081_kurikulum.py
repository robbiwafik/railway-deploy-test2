# Generated by Django 4.2.2 on 2023-07-17 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0080_matakuliah_semester'),
    ]

    operations = [
        migrations.CreateModel(
            name='Kurikulum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kode', models.CharField(max_length=10, unique=True)),
                ('nama', models.CharField(max_length=255)),
                ('tanggal_digunakan', models.DateField()),
            ],
        ),
    ]
