# Generated by Django 4.1 on 2024-07-30 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bikes', '0002_remove_rental_cost_bike_cost_per_minute_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bike',
            name='cost_per_minute',
            field=models.DecimalField(decimal_places=2, default='2.00', max_digits=5),
        ),
    ]
