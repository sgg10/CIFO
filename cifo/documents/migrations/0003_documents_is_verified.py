# Generated by Django 3.1.5 on 2021-06-03 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_auto_20210603_0229'),
    ]

    operations = [
        migrations.AddField(
            model_name='documents',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
