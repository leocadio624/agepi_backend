# Generated by Django 3.2.6 on 2022-05-19 21:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('protocol', '0002_initial'),
        ('firma', '0002_historicalfirmaprotocolo_fk_protocol'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalfirmaprotocolo',
            name='fk_user',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='pk de usuario'),
        ),
        migrations.AddField(
            model_name='historicalfirmaprotocolo',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalfirma',
            name='fk_user',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='pk de usuario'),
        ),
        migrations.AddField(
            model_name='historicalfirma',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='firmaprotocolo',
            name='fk_protocol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='protocol.protocol', verbose_name='pk de protocolo'),
        ),
        migrations.AddField(
            model_name='firmaprotocolo',
            name='fk_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='pk de usuario'),
        ),
        migrations.AddField(
            model_name='firma',
            name='fk_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='pk de usuario'),
        ),
    ]