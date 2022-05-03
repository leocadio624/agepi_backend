# Generated by Django 3.2.6 on 2022-04-30 23:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('protocol', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PeriodoEscolar',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Fecha de modificacion')),
                ('deleted_date', models.DateTimeField(auto_now=True, verbose_name='Fecha de eliminacion')),
                ('periodo', models.IntegerField(verbose_name='periodo')),
                ('anio', models.IntegerField(verbose_name='anio')),
                ('descp', models.CharField(max_length=50, verbose_name='Descripccion')),
            ],
            options={
                'verbose_name': 'Periodo escolar',
                'verbose_name_plural': 'Periodos escolares',
            },
        ),
        migrations.CreateModel(
            name='HistoricalPeriodoEscolar',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('created_date', models.DateTimeField(blank=True, editable=False, verbose_name='Fecha de creacion')),
                ('modified_date', models.DateTimeField(blank=True, editable=False, verbose_name='Fecha de modificacion')),
                ('deleted_date', models.DateTimeField(blank=True, editable=False, verbose_name='Fecha de eliminacion')),
                ('periodo', models.IntegerField(verbose_name='periodo')),
                ('anio', models.IntegerField(verbose_name='anio')),
                ('descp', models.CharField(max_length=50, verbose_name='Descripccion')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Periodo escolar',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]