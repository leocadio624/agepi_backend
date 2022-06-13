# Generated by Django 3.2.6 on 2022-06-13 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('firma', '0001_initial'),
        ('protocol', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalfirmaprotocolo',
            name='fk_protocol',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='protocol.protocol', verbose_name='pk de protocolo'),
        ),
    ]
