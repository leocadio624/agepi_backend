# Generated by Django 3.2.6 on 2022-04-24 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0003_auto_20220424_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificacion',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion'),
        ),
    ]
