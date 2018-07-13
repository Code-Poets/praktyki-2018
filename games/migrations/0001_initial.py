# Generated by Django 2.0.7 on 2018-07-13 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CharacterClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CharacterRace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=4)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('finished_at', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Gamer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nick', models.CharField(max_length=50)),
                ('winner', models.BooleanField(default=False)),
                ('level', models.IntegerField(default=0)),
                ('bonus', models.IntegerField(default=0)),
                ('gender', models.NullBooleanField(default=None)),
                ('class_slot_1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='games.CharacterClass')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gamers', to='games.Game')),
                ('race_slot_1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='games.CharacterRace')),
            ],
        ),
    ]
