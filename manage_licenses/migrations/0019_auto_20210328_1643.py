# Generated by Django 3.1.6 on 2021-03-28 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_licenses', '0018_auto_20210326_0719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='license',
            name='creation_date',
            field=models.DateField(null=True, verbose_name='Date created '),
        ),
        migrations.AlterField(
            model_name='license',
            name='expiration_date',
            field=models.DateField(null=True, verbose_name='Expiration date '),
        ),
    ]