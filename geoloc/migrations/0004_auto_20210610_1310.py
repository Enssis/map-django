# Generated by Django 2.2.12 on 2021-06-10 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geoloc', '0003_auto_20210610_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='continent',
            name='pop',
            field=models.FloatField(verbose_name='population 2005'),
        ),
    ]
