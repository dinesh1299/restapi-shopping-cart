# Generated by Django 4.2.1 on 2023-07-05 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0011_alter_rating_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='num_of_rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.FloatField(default=0),
        ),
    ]
