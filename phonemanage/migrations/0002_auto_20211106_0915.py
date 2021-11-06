# Generated by Django 3.2.8 on 2021-11-06 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phonemanage', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='roll',
        ),
        migrations.AddField(
            model_name='myuser',
            name='role',
            field=models.SmallIntegerField(choices=[(0, 'Admin'), (1, 'Staff'), (2, 'Normal user')], null=True),
        ),
    ]
