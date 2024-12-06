# Generated by Django 5.1.3 on 2024-11-30 06:17

import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='time',
            field=models.CharField(blank=True, default='30 November 2024', max_length=100),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=tinymce.models.HTMLField(),
        ),
        migrations.AlterField(
            model_name='post',
            name='time',
            field=models.CharField(blank=True, default='30 November 2024', max_length=100),
        ),
    ]
