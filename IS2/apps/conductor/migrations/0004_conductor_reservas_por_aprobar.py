# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-06-13 21:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conductor', '0003_conductor_autoaceptar_reservas'),
    ]

    operations = [
        migrations.AddField(
            model_name='conductor',
            name='reservas_por_aprobar',
            field=models.IntegerField(default=0),
        ),
    ]
