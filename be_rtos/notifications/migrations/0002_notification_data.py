# Generated by Django 5.0.6 on 2024-07-03 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='data',
            field=models.TextField(blank=True, null=True),
        ),
    ]
