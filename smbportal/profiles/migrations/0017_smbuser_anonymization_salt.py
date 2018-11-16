# Generated by Django 2.0 on 2018-11-13 12:38

from django.db import migrations, models
import profiles.models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0016_auto_20180918_0953'),
    ]

    operations = [
        migrations.AddField(
            model_name='smbuser',
            name='anonymization_salt',
            field=models.CharField(default=profiles.models.generate_anonymization_salt, editable=False, help_text='Random string used when anonymizing user data', max_length=36),
        ),
    ]