# Generated by Django 2.0.7 on 2018-09-10 08:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0006_auto_20180903_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='max_players',
            field=models.IntegerField(default=6, validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(8)]),
        ),
    ]
