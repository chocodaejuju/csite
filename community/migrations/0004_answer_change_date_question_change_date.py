# Generated by Django 4.0.3 on 2023-05-15 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0003_answer_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='change_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='change_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
