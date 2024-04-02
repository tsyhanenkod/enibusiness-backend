# Generated by Django 5.0.2 on 2024-03-31 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_customuser_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='referal',
            name='contacts',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='referal',
            name='eni',
            field=models.CharField(blank=True, default='eni', max_length=10, null=True),
        ),
    ]