# Generated by Django 4.0.5 on 2022-06-24 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promoapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='firs_name',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user_name',
        ),
    ]
