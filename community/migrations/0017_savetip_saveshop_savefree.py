# Generated by Django 4.0.3 on 2023-09-23 12:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('community', '0016_saveq'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaveTip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_savetip', to=settings.AUTH_USER_MODEL)),
                ('tip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.tip')),
            ],
        ),
        migrations.CreateModel(
            name='SaveShop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_saveshop', to=settings.AUTH_USER_MODEL)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.shopping')),
            ],
        ),
        migrations.CreateModel(
            name='SaveFree',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_savefree', to=settings.AUTH_USER_MODEL)),
                ('free', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.free')),
            ],
        ),
    ]
