from django import forms
from django.utils.translation import ugettext_lazy as _
from games.models.model_game import Game
from games.models.model_gamer import Gamer


class JoinForm(forms.Form):

    nick = forms.CharField(label=_('Nick'))                    # Text input for player's nickname
    game_pass = forms.CharField(label=_('Game access code'))   # Text input for game password

    def get_game_pass(self):
        return self.cleaned_data['game_pass']

    def get_nick(self):
        return self.cleaned_data['nick']

    def clean_game_pass(self):
       return self.cleaned_data['game_pass'].upper()

    def clean(self):
        cleaned_data = super(JoinForm, self).clean()
        game_pass = self.cleaned_data['game_pass']
        nick = self.cleaned_data['nick']
        user = self.initial['user']
        gamer_id = self.initial['gamer_id']

        try:
            game = Game.objects.get(game_code=game_pass)  # Find game by code

        except Game.DoesNotExist:
            raise forms.ValidationError(_('WHOOPS! No such game could be found!'))

        logged_gamer = None
        nonlogged_gamer = None
        if user is not None:
            logged_gamer = Gamer.objects.filter(game=game, user=user)
        else:
            nonlogged_gamer = Gamer.objects.filter(game=game, id=gamer_id)

        if logged_gamer or nonlogged_gamer:
            raise forms.ValidationError(_('You have already joined this game!'))

        if game.is_finished():
            raise forms.ValidationError(_('Sorry, this game has already finished.'))
        if not game.is_available():
            raise forms.ValidationError(_('Sorry, no more places available. :-('))

        gamers = game.gamers.all()

        for gamer in gamers:
            if gamer.nick == nick:
                raise forms.ValidationError(_('This nickname has already been taken. :-('))
        return cleaned_data
