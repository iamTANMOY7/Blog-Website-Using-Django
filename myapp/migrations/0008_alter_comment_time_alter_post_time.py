# Generated by Django 5.1.3 on 2024-11-30 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_remove_post_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='time',
            field=models.CharField(blank=True, default='01 December 2024', max_length=100),
        ),
        migrations.AlterField(
            model_name='post',
            name='time',
            field=models.CharField(blank=True, default='01 December 2024', max_length=100),
        ),
    ]
