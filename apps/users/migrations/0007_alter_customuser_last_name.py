# Generated by Django 5.0.2 on 2024-03-13 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_requesteduser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
