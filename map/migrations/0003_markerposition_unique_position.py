# Generated by Django 4.0.3 on 2023-09-02 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0002_markerposition_content'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='markerposition',
            constraint=models.UniqueConstraint(fields=('lat', 'lng'), name='unique_position'),
        ),
    ]
