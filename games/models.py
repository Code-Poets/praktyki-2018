from django.db import models

MAX_PLAYERS = 8


# Create your models here.
class Game(models.Model):
    # host = models.ForeignKey(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True)

    def is_available(self):
        gamers = self.gamers.count()
        if gamers < MAX_PLAYERS:
            return True
        return False


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


class Gamer(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='gamers')
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    nick = models.CharField(max_length=50, unique=False)
    winner = models.BooleanField(default=False)
    level = models.IntegerField(default=0)
    bonus = models.IntegerField(default=0)
    gender = models.NullBooleanField(default=None)
    race_slot_1 = models.ForeignKey(CharacterRace, null=True, on_delete=models.SET_NULL)
    # race_slot_2 = models.ForeignKey(Race, null=True, on_delete=models.SET_NULL)
    class_slot_1 = models.ForeignKey(CharacterClass, null=True, on_delete=models.SET_NULL)
    # class_slot_2 = models.ForeignKey(CClass, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.nick
