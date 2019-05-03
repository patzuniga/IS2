# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-05-03 09:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conductor', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conductor',
            name='licencia',
        ),
        migrations.RemoveField(
            model_name='vehiculo',
            name='pantete',
        ),
        migrations.AddField(
            model_name='vehiculo',
            name='Numeroasientos',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='vehiculo',
            name='color',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='vehiculo',
            name='consumo',
            field=models.IntegerField(default=10),
        ),
        migrations.AddField(
            model_name='vehiculo',
            name='foto',
            field=models.ImageField(null=True, upload_to='autos'),
        ),
        migrations.AddField(
            model_name='vehiculo',
            name='patente',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='vehiculo',
            name='maleta',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='vehiculo',
            name='marca',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='vehiculo',
            name='modelo',
            field=models.CharField(max_length=30, null=True),
        ),
    ]