# Generated by Django 3.1.5 on 2021-02-16 05:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0003_userssessions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userssessions',
            name='ended',
        ),
    ]
