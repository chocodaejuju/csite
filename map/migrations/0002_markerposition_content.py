# Generated by Django 4.0.3 on 2023-08-28 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='markerposition',
            name='content',
            field=models.TextField(default='마커 내용'),
        ),
    ]
