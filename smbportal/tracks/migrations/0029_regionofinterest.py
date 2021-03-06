# Generated by Django 2.0 on 2018-10-08 11:55

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0028_auto_20180917_1613'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegionOfInterest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(help_text='Geometry for the region of interest. Only points that are located within this area will be considered when creating tracks', srid=4326, verbose_name='geometry')),
            ],
        ),
    ]
