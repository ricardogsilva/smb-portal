# Generated by Django 2.0.5 on 2018-06-08 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0006_auto_20180607_2120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bike',
            name='nickname',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
