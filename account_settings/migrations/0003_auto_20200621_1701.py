# Generated by Django 3.0.7 on 2020-06-21 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_settings', '0002_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, max_length=200),
        ),
    ]
