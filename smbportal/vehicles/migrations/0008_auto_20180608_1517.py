# Generated by Django 2.0.5 on 2018-06-08 15:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vehicles', '0007_auto_20180608_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bike',
            name='nickname',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name='bike',
            unique_together={('owner', 'nickname')},
        ),
    ]
