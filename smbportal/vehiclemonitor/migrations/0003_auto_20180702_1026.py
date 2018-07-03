# Generated by Django 2.0.5 on 2018-07-02 10:26

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('vehiclemonitor', '0002_auto_20180613_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bikeobservation',
            name='address',
            field=models.CharField(blank=True, help_text='Approximate address. Either this field or `position` must be given', max_length=255, verbose_name='address'),
        ),
        migrations.AlterField(
            model_name='bikeobservation',
            name='bike',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='observations', to='vehicles.Bike', verbose_name='bike'),
        ),
        migrations.AlterField(
            model_name='bikeobservation',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='bikeobservation',
            name='details',
            field=models.TextField(blank=True, verbose_name='details'),
        ),
        migrations.AlterField(
            model_name='bikeobservation',
            name='observed_at',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='When the observation was made', verbose_name='observed at'),
        ),
        migrations.AlterField(
            model_name='bikeobservation',
            name='position',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, help_text='Either this field or `address` must be given', null=True, srid=4326, verbose_name='position'),
        ),
        migrations.AlterField(
            model_name='bikeobservation',
            name='reporter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='reporter'),
        ),
    ]