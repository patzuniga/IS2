# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-06-15 22:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viaje', '0013_auto_20190615_2222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tramo',
            name='fecha',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='tramo',
            name='hora_llegada',
            field=models.TimeField(default='15:00'),
        ),
        migrations.AlterField(
            model_name='tramo',
            name='hora_salida',
            field=models.TimeField(default='15:00'),
        ),
    ]
