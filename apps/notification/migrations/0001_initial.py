# Generated by Django 3.2.6 on 2022-04-30 02:39

from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalTipoNotificacion',
            fields=[
                ('id', models.IntegerField(db_index=True)),
                ('descp', models.CharField(max_length=255, verbose_name='Descripccion de la notificacion')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical Tipo de notificacion',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='TipoNotificacion',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('descp', models.CharField(max_length=255, verbose_name='Descripccion de la notificacion')),
            ],
            options={
                'verbose_name': 'Tipo de notificacion',
                'verbose_name_plural': 'Tipo de notificaciones',
            },
        ),
        migrations.CreateModel(
            name='NotificacionTeam',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Fecha de modificacion')),
                ('deleted_date', models.DateTimeField(auto_now=True, verbose_name='Fecha de eliminacion')),
                ('fk_tipoNotificacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notification.tiponotificacion', verbose_name='pk tipo de notificacion')),
            ],
            options={
                'verbose_name': 'Notificacion equipo',
                'verbose_name_plural': 'Notificaciones equipo',
            },
        ),
    ]
