# Generated by Django 2.2.7 on 2019-11-05 07:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thoth_data_collector', '0007_auto_20191105_0641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paperitem',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 5, 7, 1, 49, 955783)),
        ),
        migrations.AlterField(
            model_name='paperitem',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 5, 7, 1, 49, 955825)),
        ),
    ]
