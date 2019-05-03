# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-05-03 14:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('viaje', '0002_auto_20190503_1458'),
        ('conductor', '0004_auto_20190503_1434'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conductor',
            name='viaje',
        ),
        migrations.AddField(
            model_name='conductor',
            name='viajes',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='_viajes', to='viaje.Viaje'),
        ),
    ]