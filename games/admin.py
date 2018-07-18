from django.contrib import admin

from .models import Game, Gamer, CharacterClass, CharacterRace


class GamerInline(admin.TabularInline):
    model = Gamer
    extra = 1


class GameAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['password']}),
    ]
    inlines = [GamerInline]
    list_display = ('password', 'created_at', 'finished_at')
    list_filter = ['created_at']
    search_fields = ['password']


admin.site.register(Game, GameAdmin)
admin.site.register(Gamer)
admin.site.register(CharacterClass)
admin.site.register(CharacterRace)
