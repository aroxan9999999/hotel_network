# Generated by Django 3.1.7 on 2023-04-03 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotel_app', '0007_auto_20230403_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tour',
            name='hotel_to_tour',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_tour_to_hotel', to='hotel_app.hotel'),
        ),
    ]
