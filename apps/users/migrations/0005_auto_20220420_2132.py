# Generated by Django 3.2.6 on 2022-04-21 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20220418_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaluser',
            name='code_activate',
            field=models.CharField(blank=True, default='', max_length=8, null=True),
        ),
        migrations.AddField(
            model_name='historicaluser',
            name='code_activate_confirm',
            field=models.CharField(blank=True, default='', max_length=8, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='code_activate',
            field=models.CharField(blank=True, default='', max_length=8, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='code_activate_confirm',
            field=models.CharField(blank=True, default='', max_length=8, null=True),
        ),
    ]
