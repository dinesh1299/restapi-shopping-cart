# Generated by Django 4.2.1 on 2023-07-06 05:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0013_rating_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='order',
        ),
        migrations.AddField(
            model_name='rating',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ratings', to='first_app.product'),
        ),
    ]
