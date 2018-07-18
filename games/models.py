from django.db import models
from users.models import CustomUser
from django.core.validators import MaxValueValidator, MinValueValidator
from enum import Enum, unique


# Create your models here.
class Game(models.Model):
    host = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    game_code = models.CharField(max_length=4)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, default=None)
    max_players = models.IntegerField(default=6, validators=[MinValueValidator(2), MaxValueValidator(8)])
    winning_level = models.IntegerField(default=10, validators=[MinValueValidator(1)])

    def is_available(self):
        gamers = self.gamers.count()
        return gamers < self.max_players

    def is_finished(self):
        return self.finished_at is not None


class CharacterRace(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=1000, unique=True)

    def __str__(self):
        return self.name


class CharacterClass(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=1000, unique=True)

    def __str__(self):
        return self.name


@unique
class Gender(Enum):
    F = 'Female'
    M = 'Male'
    N = 'None'

GENDER_CHOICES = (
    (Gender.F.value,    'Female'),
    (Gender.M.value,    'Male'),
    (Gender.N.value,    'None'),
)
assert set(s.value for s in Gender) == set(dict(GENDER_CHOICES))


class Gamer(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='gamers')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, default=None)
    nick = models.CharField(max_length=50, unique=False)
    winner = models.BooleanField(default=False)
    level = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    bonus = models.IntegerField(default=0)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default = Gender.N.value)
    race_slot_1 = models.ForeignKey(CharacterRace, null=True, on_delete=models.SET_NULL, related_name='race_slot_1', default=None)
    race_slot_2 = models.ForeignKey(CharacterRace, null=True, on_delete=models.SET_NULL, related_name='race_slot_2', default=None)
    class_slot_1 = models.ForeignKey(CharacterClass, null=True, on_delete=models.SET_NULL, related_name='class_slot_1', default=None)
    class_slot_2 = models.ForeignKey(CharacterClass, null=True, on_delete=models.SET_NULL, related_name='class_slot_2', default=None)
    #races = models.ManyToManyField(CharacterRace)
    #classes = models.ManyToManyField(CharacterClass)

    def __str__(self):
        return self.nick

    def is_potential_winner(self):
        return self.level >= self.game.winning_level