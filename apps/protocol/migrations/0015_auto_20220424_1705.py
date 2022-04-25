# Generated by Django 3.2.6 on 2022-04-24 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protocol', '0014_auto_20220407_0140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalkeyword',
            name='created_date',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Fecha de creacion'),
        ),
        migrations.AlterField(
            model_name='historicalprotocol',
            name='created_date',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Fecha de creacion'),
        ),
        migrations.AlterField(
            model_name='historicalprotocolstate',
            name='created_date',
            field=models.DateTimeField(blank=True, editable=False, verbose_name='Fecha de creacion'),
        ),
        migrations.AlterField(
            model_name='keyword',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion'),
        ),
        migrations.AlterField(
            model_name='protocol',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion'),
        ),
        migrations.AlterField(
            model_name='protocolstate',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion'),
        ),
    ]
