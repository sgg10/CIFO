# Generated by Django 3.1.5 on 2021-05-27 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='identification',
            field=models.BigIntegerField(),
        ),
    ]