# Generated by Django 5.0.2 on 2024-03-06 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_referal'),
    ]

    operations = [
        migrations.AddField(
            model_name='temporaryuser',
            name='group',
            field=models.CharField(max_length=5, null=True),
        ),
    ]
