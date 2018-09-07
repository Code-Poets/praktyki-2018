from django.contrib import admin

from games.models.model_game import Game
from games.models.model_gamer import Gamer
from games.models.model_character_race import CharacterRace
from games.models.model_character_class import CharacterClass


class GamerInline(admin.TabularInline):
    model = Gamer
    extra = 1


class GameAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['game_code']}),
    ]
    inlines = [GamerInline]
    list_display = ('game_code', 'created_at', 'finished_at')
    list_filter = ['created_at']
    search_fields = ['game_code']


admin.site.register(Game, GameAdmin)
admin.site.register(Gamer)
admin.site.register(CharacterClass)
admin.site.register(CharacterRace)
