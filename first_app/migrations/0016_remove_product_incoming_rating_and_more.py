# Generated by Django 4.2.1 on 2023-07-06 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0015_product_incoming_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='incoming_rating',
        ),
        migrations.AddField(
            model_name='product',
            name='itotal_rating_sum',
            field=models.FloatField(default=0),
        ),
    ]
