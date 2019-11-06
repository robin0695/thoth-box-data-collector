# Generated by Django 2.2.5 on 2019-11-05 11:28

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('thoth_data_collector', '0006_auto_20191104_0647'),
    ]

    operations = [
        migrations.CreateModel(
            name='IssueInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_title', models.CharField(max_length=1000)),
                ('issue_date', models.DateTimeField(default=datetime.datetime(2019, 11, 5, 11, 28, 32, 958273))),
                ('issue_sn', models.CharField(max_length=100)),
                ('created_date', models.DateTimeField(default=datetime.datetime(2019, 11, 5, 11, 28, 32, 958316))),
                ('created_by', models.CharField(default='', max_length=200)),
                ('update_date', models.DateTimeField(default=datetime.datetime(2019, 11, 5, 11, 28, 32, 958341))),
                ('update_by', models.CharField(default='', max_length=200)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='paperitem',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 5, 11, 28, 32, 958862)),
        ),
        migrations.AlterField(
            model_name='paperitem',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 5, 11, 28, 32, 958889)),
        ),
        migrations.AddField(
            model_name='paperitem',
            name='issue_info',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, related_name='papers', to='thoth_data_collector.IssueInfo'),
        ),
    ]
