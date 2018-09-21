from django.db import models
from users.models import CustomUser
from django.core.validators import MaxValueValidator, MinValueValidator


MAX_GAMERS_PER_GAME = 8
MIN_GAMERS_PER_GAME = 2
DEFAULT_GAMERS_PER_GAME = 6
MIN_WINNING_LEVEL = 1
DEFAULT_WINNING_LEVEL = 10
GAME_CODE_LENGTH = 4


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
