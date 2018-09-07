from django.db import models


class CharacterRace(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=1000, unique=True)

    def __str__(self):
        return self.name
