# Generated by Django 3.2.6 on 2022-04-16 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comunidad', '0002_auto_20220416_0154'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alumno',
            old_name='fk_team',
            new_name='fk_programa',
        ),
    ]