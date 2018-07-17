from django.db import models
from users.models import CustomUser
from django.core.validators import MaxValueValidator, MinValueValidator
from enum import Enum


# Create your models here.
class Game(models.Model):
    host = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    game_code = models.CharField(max_length=4)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, default=None)
    max_players = models.IntegerField(default=2, validators=[MinValueValidator(2)])

    def is_available(self):
        gamers = self.gamers.count()
        return gamers < self.max_players

    def is_finished(self):
        return self.finished_at


class CharacterRace(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class CharacterClass(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


"""
class Gender(Enum):
    F = 'Female'
    M = 'Male'
    N = 'None'
"""


class Gamer(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='gamers')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, default=None)
    nick = models.CharField(max_length=50, unique=False)
    winner = models.BooleanField(default=False)
    level = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    bonus = models.IntegerField(default=0)
    gender = models.NullBooleanField(default=None)
    race_slot_1 = models.ForeignKey(CharacterRace, null=True, on_delete=models.SET_NULL,
                                    related_name='race_slot_1', default=None)
    race_slot_2 = models.ForeignKey(CharacterRace, null=True, on_delete=models.SET_NULL,
                                    related_name='race_slot_2', default=None)
    class_slot_1 = models.ForeignKey(CharacterClass, null=True, on_delete=models.SET_NULL,
                                     related_name='class_slot_1', default=None)
    class_slot_2 = models.ForeignKey(CharacterClass, null=True, on_delete=models.SET_NULL,
                                     related_name='class_slot_2', default=None)

    def __str__(self):
        return self.nick
