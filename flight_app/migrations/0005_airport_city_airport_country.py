# Generated by Django 4.0.2 on 2022-02-14 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight_app', '0004_create_ES_mapping'),
    ]

    operations = [
        migrations.AddField(
            model_name='airport',
            name='city',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='airport',
            name='country',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
