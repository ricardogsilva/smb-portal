# Generated by Django 2.0 on 2018-08-10 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0015_segment_vehicle_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='segment',
            name='track',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='segments', to='tracks.Track', verbose_name='track'),
        ),
    ]