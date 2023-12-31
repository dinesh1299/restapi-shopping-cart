# Generated by Django 4.2.1 on 2023-07-04 10:08

from django.db import migrations, models
import django.db.models.deletion
import first_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0009_order_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(validators=[first_app.models.validate_less_than_or_equal_to_five])),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='first_app.order')),
            ],
        ),
    ]
