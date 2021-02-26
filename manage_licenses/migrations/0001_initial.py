# Generated by Django 3.1.6 on 2021-02-19 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org_id', models.IntegerField(null=True)),
                ('product_name', models.CharField(max_length=50)),
                ('version', models.IntegerField(null=True)),
                ('creator_address', models.CharField(max_length=50, verbose_name='Created by ')),
                ('creation_date', models.DateTimeField(verbose_name='Date Created')),
            ],
        ),
    ]
