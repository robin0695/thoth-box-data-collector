# Generated by Django 2.2.5 on 2019-11-04 06:47

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('thoth_data_collector', '0005_auto_20191102_1303'),
    ]

    operations = [
        migrations.AddField(
            model_name='paperitem',
            name='is_processed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='paperauthor',
            name='paper_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authors', to='thoth_data_collector.PaperItem'),
        ),
        migrations.AlterField(
            model_name='papercategory',
            name='paper_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='thoth_data_collector.PaperItem'),
        ),
        migrations.AlterField(
            model_name='paperitem',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 4, 6, 47, 40, 845299)),
        ),
        migrations.AlterField(
            model_name='paperitem',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 4, 6, 47, 40, 845338)),
        ),
    ]
