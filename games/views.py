from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from .models import Game, Gamer


# Create your views here.
class GamerView(generic.DetailView):
    model = Gamer
    template_name = 'game/gamer.html'

    def get_queryset(self):
        return Gamer.objects


class GameAccessView(generic.FormView):
    template_name = 'game/game_access.html'


def join_game(request, game_pass, nick):
    game = get_object_or_404(Game, password=game_pass)

    gamer_id = None
    HttpResponseRedirect('game/gamer', gamer_id)


def update_stats(request, gamer_id):
    HttpResponseRedirect('game/gamer', gamer_id)