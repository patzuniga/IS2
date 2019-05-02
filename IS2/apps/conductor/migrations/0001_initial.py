# Generated by Django 2.2 on 2019-05-02 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('viaje', '0001_initial'),
        ('usuario', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conductor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('licencia', models.IntegerField()),
                ('clasedelicencia', models.CharField(max_length=1)),
                ('fecha_obtencion', models.CharField(max_length=30)),
                ('marca', models.CharField(max_length=30)),
                ('modelo', models.CharField(max_length=30)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.Usuario')),
                ('viaje', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='viaje.Viaje')),
            ],
        ),
    ]
