# Generated by Django 2.2.5 on 2019-10-27 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thoth_data_collector', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='papercategory',
            name='is_primary',
            field=models.BooleanField(default=False),
        ),
    ]
