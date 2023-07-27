# Generated by Django 4.1.7 on 2023-03-06 02:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0013_mahasiswa'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ruangan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=255)),
                ('gedung', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.gedungkuliah')),
            ],
        ),
    ]
