from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from games.models.model_game import Game
from games.models.model_gamer import Gamer


def update_stats(request, pk):
    game = Game.objects.get(pk=pk)
    gamers = Gamer.objects.filter(game__game_code=game.game_code).order_by('level')

    for gamer in gamers:
        if gamer.level >= game.winning_level:
            gamer.winner = True
            gamer.save()

    game.finished_at = timezone.now()
    game.game_code = None
    game.save()
    return HttpResponseRedirect(reverse('home'))
