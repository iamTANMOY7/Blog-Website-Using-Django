# Generated by Django 5.1.3 on 2024-11-30 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_alter_comment_time_alter_post_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('Programming', 'Programming'), ('Travel', 'Travel'), ('Education', 'Education'), ('Technology', 'Technology'), ('Artificial Intelligence', 'Artificial_Intelligence')], max_length=600),
        ),
    ]
