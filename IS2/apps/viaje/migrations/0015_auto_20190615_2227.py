# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-06-15 22:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viaje', '0014_auto_20190615_2227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tramo',
            name='fecha',
            field=models.DateField(),
        ),
    ]
