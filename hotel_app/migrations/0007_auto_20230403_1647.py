# Generated by Django 3.1.7 on 2023-04-03 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotel_app', '0006_tour_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tour',
            old_name='hotel',
            new_name='hotel_to_tour',
        ),
    ]
