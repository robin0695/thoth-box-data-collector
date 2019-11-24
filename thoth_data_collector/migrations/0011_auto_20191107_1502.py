# Generated by Django 2.2.5 on 2019-11-07 15:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thoth_data_collector', '0010_auto_20191105_1132'),
    ]

    operations = [
        migrations.AddField(
            model_name='paperitem',
            name='summary',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='issueinfo',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 7, 15, 2, 12, 328642)),
        ),
        migrations.AlterField(
            model_name='issueinfo',
            name='issue_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 7, 15, 2, 12, 328554)),
        ),
        migrations.AlterField(
            model_name='issueinfo',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 7, 15, 2, 12, 328699)),
        ),
        migrations.AlterField(
            model_name='paperitem',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 7, 15, 2, 12, 329878)),
        ),
        migrations.AlterField(
            model_name='paperitem',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 7, 15, 2, 12, 329934)),
        ),
    ]
