# Generated by Django 4.2.2 on 2023-07-05 13:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0072_programstudi_akreditasi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jadwalmakul',
            name='dosen',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='makul_ajar', to='academic.dosen'),
        ),
    ]