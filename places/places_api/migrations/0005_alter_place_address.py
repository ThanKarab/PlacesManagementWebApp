# Generated by Django 4.1.5 on 2023-01-08 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places_api', '0004_alter_place_name_alter_place_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='address',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
