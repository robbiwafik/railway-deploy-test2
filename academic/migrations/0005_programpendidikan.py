# Generated by Django 4.1.7 on 2023-03-01 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0004_alter_semester_no'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgramPendidikan',
            fields=[
                ('kode', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('nama', models.CharField(max_length=255)),
            ],
        ),
    ]
