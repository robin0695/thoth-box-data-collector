# Generated by Django 2.2.7 on 2019-11-05 06:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thoth_data_collector', '0006_auto_20191104_0647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paperitem',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 5, 6, 41, 2, 767688)),
        ),
        migrations.AlterField(
            model_name='paperitem',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 5, 6, 41, 2, 768575)),
        ),
    ]
