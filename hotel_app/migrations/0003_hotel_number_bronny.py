# Generated by Django 3.1.7 on 2023-04-02 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel_app', '0002_auto_20230402_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel_number',
            name='bronny',
            field=models.BooleanField(default=False),
        ),
    ]