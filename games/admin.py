from django.contrib import admin

from .models import Game, Gamer, CharacterClass, CharacterRace

admin.site.register(Game)
admin.site.register(Gamer)
admin.site.register(CharacterClass)
admin.site.register(CharacterRace)
