# Generated by Django 2.2.7 on 2019-12-03 11:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('thoth_data_collector', '0015_auto_20191203_1059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paperitem',
            name='last_view_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 3, 11, 0, 14, 160246, tzinfo=utc)),
        ),
    ]
