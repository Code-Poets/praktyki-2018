from django.db import models
from users.models import CustomUser
from django.core.validators import MaxValueValidator, MinValueValidator
from enum import Enum, unique

MAX_GAMERS_PER_GAME = 8
MIN_GAMERS_PER_GAME = 6
DEFAULT_GAMERS_PER_GAME = MIN_GAMERS_PER_GAME
MIN_WINNING_LEVEL = 1
DEFAULT_WINNING_LEVEL = 10
GAME_CODE_LENGTH = 4


# Create your models here.
class Game(models.Model):
    host = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    game_code = models.CharField(max_length=GAME_CODE_LENGTH, null=True, blank=True)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, default=None, blank=True)
    max_players = models.IntegerField(default=DEFAULT_GAMERS_PER_GAME,
                                      validators=[MinValueValidator(MIN_GAMERS_PER_GAME),
                                                  MaxValueValidator(MAX_GAMERS_PER_GAME)])
    winning_level = models.IntegerField(default=DEFAULT_WINNING_LEVEL, validators=[MinValueValidator(MIN_WINNING_LEVEL)])

    def __str__(self):
        return str(self.pk) + ' ' + self.name

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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, default=None, blank=True)
    nick = models.CharField(max_length=50, unique=False)
    winner = models.BooleanField(default=False)
    level = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    bonus = models.IntegerField(default=0)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default=Gender.N.value)
    race_slot_1 = models.ForeignKey(CharacterRace, null=True, on_delete=models.SET_NULL,
                                    related_name='race_slot_1', default=None, blank=True)
    race_slot_2 = models.ForeignKey(CharacterRace, null=True, on_delete=models.SET_NULL,
                                    related_name='race_slot_2', default=None, blank=True)
    class_slot_1 = models.ForeignKey(CharacterClass, null=True, on_delete=models.SET_NULL,
                                     related_name='class_slot_1', default=None, blank=True)
    class_slot_2 = models.ForeignKey(CharacterClass, null=True, on_delete=models.SET_NULL,
                                     related_name='class_slot_2', default=None, blank=True)
    # races = models.ManyToManyField(CharacterRace)
    # classes = models.ManyToManyField(CharacterClass)

    def __str__(self):
        return self.nick

    def is_potential_winner(self):
        return self.level >= self.game.winning_level
