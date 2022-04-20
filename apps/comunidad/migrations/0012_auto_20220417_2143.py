# Generated by Django 3.2.6 on 2022-04-18 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comunidad', '0011_auto_20220417_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumno',
            name='boleta',
            field=models.CharField(max_length=255, unique=True, verbose_name='Boleta'),
        ),
        migrations.AlterField(
            model_name='alumno',
            name='email',
            field=models.EmailField(max_length=255, unique=True, verbose_name='Correo Electronico'),
        ),
    ]