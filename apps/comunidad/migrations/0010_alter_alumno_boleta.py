# Generated by Django 3.2.6 on 2022-04-18 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comunidad', '0009_profesor_alta_app'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumno',
            name='boleta',
            field=models.CharField(max_length=255, unique=True, verbose_name='Boleta'),
        ),
    ]