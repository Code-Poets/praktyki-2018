from django.db import models
from .model_character_class import CharacterClass
from .model_character_race import CharacterRace
from .model_game import Game, MAX_GAMERS_PER_GAME
from .enum_gender import Gender, GENDER_CHOICES
from users.models import CustomUser
from django.core.validators import MaxValueValidator, MinValueValidator


class Gamer(models.Model):
    class Meta:
        ordering = ['id']
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='gamers')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, default=None, blank=True)
    nick = models.CharField(max_length=50, unique=False)
    winner = models.BooleanField(default=False)
    status = models.CharField(max_length=30, null=True, default=None, blank=True)
    order = models.IntegerField(validators=[MinValueValidator(1),
                                            MaxValueValidator(MAX_GAMERS_PER_GAME)],
                                null=True, blank=True)
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
