# Generated by Django 3.0.7 on 2020-06-22 12:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account_settings', '0006_auto_20200622_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilephoto',
            name='uploaded_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]
