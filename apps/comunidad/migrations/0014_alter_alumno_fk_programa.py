# Generated by Django 3.2.6 on 2022-04-22 16:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comunidad', '0013_alter_alumno_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumno',
            name='fk_programa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comunidad.programaacademico', verbose_name='pk de programa academico'),
        ),
    ]