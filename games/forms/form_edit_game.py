from django import forms
from django.utils.translation import ugettext_lazy as _
from games.models import Game


class EditGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'max_players', 'winning_level']
    name = forms.CharField(label=_("Name"))
    max_players = forms.IntegerField(label=_("Players number"), min_value=2, max_value=8, initial=6)
    winning_level = forms.IntegerField(label=_("Finish at level"), min_value=1, initial=10)
