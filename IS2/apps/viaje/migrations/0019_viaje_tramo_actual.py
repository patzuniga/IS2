# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-07-05 02:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viaje', '0018_auto_20190615_2254'),
    ]

    operations = [
        migrations.AddField(
            model_name='viaje',
            name='tramo_actual',
            field=models.IntegerField(default=0),
        ),
    ]
