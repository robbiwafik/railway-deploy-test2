# Generated by Django 4.1.7 on 2023-03-01 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0002_semester'),
    ]

    operations = [
        migrations.AlterField(
            model_name='semester',
            name='no',
            field=models.PositiveSmallIntegerField(primary_key=True, serialize=False),
        ),
    ]