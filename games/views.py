# from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect  # , Http404
from django.views import generic
from django.urls import reverse
from .models import Game, Gamer
from django import forms


class GamerView(generic.DetailView):                        # GUI for player's stats in current game
    model = Gamer
    template_name = 'games/gamer.html'

    def get_queryset(self):
        return Gamer.objects


class JoinForm(forms.Form):
    nick = forms.CharField(label='Nick')                    # Text input for player's nickname
    game_pass = forms.CharField(label='Game access code')   # Text input for game password

    def get_game_pass(self):
        return self.data['game_pass']

    def get_nick(self):
        return self.data['nick']


class GameAccessView(generic.FormView):                     # GUI for joining existing game
    template_name = 'games/game_access.html'
    form_class = JoinForm

    def form_valid(self, form):                             # Pass nickname and password to join_game view
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        game_pass = form.get_game_pass()
        nick = form.get_nick()
        return HttpResponseRedirect(reverse('games:join_game', args=(game_pass, nick)))


def join_game(request, gamepass, nick):                     # View for assigning player to game
    try:
        game = Game.objects.get(password=gamepass)          # Find player by nickname in existing players
        '(Once I figure out the User support I will add here some code to check if nick is already taken :P)'
    except Game.DoesNotExist:
        return HttpResponse('WHOOPS! No such game could be found!')
    try:
        # from ipdb import set_trace; set_trace()
        gamer = game.gamers.get(nick=nick)                  # Find player by nickname in existing players
    except Gamer.DoesNotExist:
        if game.is_available():
            gamer = Gamer.objects.create(                   # Create player and add to game if possible
                game=game,
                #user=,
                nick=nick,
                winner=False,
                level=0,
                bonus=0,
                gender=None,
                race_slot_1=None,
                class_slot_1=None
            )
        else:
            return HttpResponse('Sorry, no more places available. :-(')

    return HttpResponseRedirect(reverse('games:gamer', args=(gamer.id,)))


def update_stats(request, gamer_id):
    return HttpResponseRedirect(reverse('games:gamer', args=(gamer_id,)))
