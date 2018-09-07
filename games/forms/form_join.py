from django import forms
from django.utils.translation import ugettext_lazy as _
from games.models import Game, Gamer


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

        try:
            game = Game.objects.get(game_code=game_pass)  # Find game by code

        except Game.DoesNotExist:
            raise forms.ValidationError(_('WHOOPS! No such game could be found!'))

        if user is not None:
            logged_gamer = Gamer.objects.filter(game=game, user=user)

            if logged_gamer:
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
