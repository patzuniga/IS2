# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-06-12 19:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viaje', '0010_merge_20190611_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tramo',
            name='hora_llegada',
            field=models.TimeField(default='15:00', max_length=30),
        ),
        migrations.AlterField(
            model_name='tramo',
            name='hora_salida',
            field=models.TimeField(default='15:00', max_length=30),
        ),
    ]