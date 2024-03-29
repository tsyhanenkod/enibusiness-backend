# Generated by Django 5.0.2 on 2024-02-28 20:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Referal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.CharField(blank=True, max_length=250, null=True)),
                ('amount', models.CharField(blank=True, max_length=250, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('refered_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='refered_user', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
