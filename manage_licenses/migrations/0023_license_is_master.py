# Generated by Django 3.1.6 on 2021-04-09 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_licenses', '0022_auto_20210408_1906'),
    ]

    operations = [
        migrations.AddField(
            model_name='license',
            name='is_master',
            field=models.BooleanField(default=None, null=True),
        ),
    ]
