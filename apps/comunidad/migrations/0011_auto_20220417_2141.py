# Generated by Django 3.2.6 on 2022-04-18 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comunidad', '0010_alter_alumno_boleta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumno',
            name='boleta',
            field=models.CharField(max_length=255, verbose_name='Boleta'),
        ),
        migrations.AlterField(
            model_name='alumno',
            name='email',
            field=models.EmailField(max_length=255, verbose_name='Correo Electronico'),
        ),
    ]