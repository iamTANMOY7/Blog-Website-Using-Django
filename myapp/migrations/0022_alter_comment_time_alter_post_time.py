# Generated by Django 5.1.3 on 2024-12-13 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0021_alter_comment_time_alter_post_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='time',
            field=models.CharField(blank=True, default='14 December 2024', max_length=100),
        ),
        migrations.AlterField(
            model_name='post',
            name='time',
            field=models.CharField(blank=True, default='14 December 2024', max_length=100),
        ),
    ]
