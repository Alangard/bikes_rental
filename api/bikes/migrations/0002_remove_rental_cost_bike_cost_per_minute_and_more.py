# Generated by Django 4.1 on 2024-07-30 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bikes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rental',
            name='cost',
        ),
        migrations.AddField(
            model_name='bike',
            name='cost_per_minute',
            field=models.DecimalField(decimal_places=2, default=2.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='rental',
            name='total_cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
