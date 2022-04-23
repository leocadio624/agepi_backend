# Generated by Django 3.2.6 on 2022-04-23 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0009_auto_20220422_1212'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requestteam',
            name='fk_team',
        ),
        migrations.RemoveField(
            model_name='requestteam',
            name='fk_user',
        ),
        migrations.AddField(
            model_name='historicalteammembers',
            name='solicitudEquipo',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='teammembers',
            name='solicitudEquipo',
            field=models.IntegerField(default=2),
        ),
        migrations.DeleteModel(
            name='HistoricalRequestTeam',
        ),
        migrations.DeleteModel(
            name='RequestTeam',
        ),
    ]
