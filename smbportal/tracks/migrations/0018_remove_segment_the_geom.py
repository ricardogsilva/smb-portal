# Generated by Django 2.0 on 2018-08-29 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0017_segment_geom'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='segment',
            name='the_geom',
        ),
    ]