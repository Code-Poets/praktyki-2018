# Generated by Django 2.0.7 on 2018-07-18 17:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='winning_level',
            field=models.IntegerField(default=10, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='characterclass',
            name='description',
            field=models.CharField(max_length=1000, unique=True),
        ),
        migrations.AlterField(
            model_name='characterrace',
            name='description',
            field=models.CharField(max_length=1000, unique=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='max_players',
            field=models.IntegerField(default=6, validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(8)]),
        ),
        migrations.AlterField(
            model_name='gamer',
            name='gender',
            field=models.CharField(choices=[('Female', 'Female'), ('Male', 'Male'), ('None', 'None')], default='None', max_length=20),
        ),
    ]
