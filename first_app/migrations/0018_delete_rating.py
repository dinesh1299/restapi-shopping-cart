# Generated by Django 4.2.1 on 2023-07-06 06:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0017_rename_itotal_rating_sum_product_total_rating_sum'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Rating',
        ),
    ]