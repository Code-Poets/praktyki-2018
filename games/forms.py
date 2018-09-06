from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Game, Gamer, CharacterRace, CharacterClass, GENDER_CHOICES


class GamerForm(forms.ModelForm):
    class Meta:
        model = Gamer
        fields = ['status', 'level', 'bonus', 'gender', 'race_slot_1', 'race_slot_2', 'class_slot_1', 'class_slot_2']
    status = forms.CharField(label=_('Status'), required=False)
    level = forms.IntegerField(label=_('Level'), initial=1, min_value=1)
    bonus = forms.IntegerField(label=_('Bonus'), initial=0)
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    race_slot_1 = forms.ModelChoiceField(queryset=CharacterRace.objects.all(), required=False, label=_('Race'))
    race_slot_2 = forms.ModelChoiceField(queryset=CharacterRace.objects.all(), required=False)
    class_slot_1 = forms.ModelChoiceField(queryset=CharacterClass.objects.all(), required=False, label=_('Class'))
    class_slot_2 = forms.ModelChoiceField(queryset=CharacterClass.objects.all(), required=False)

    def clean(self):
        cleaned_data = super(GamerForm, self).clean()

        race1 = cleaned_data['race_slot_1']
        race2 = cleaned_data['race_slot_2']
        class1 = cleaned_data['class_slot_1']
        class2 = cleaned_data['class_slot_2']

        if class2 is not None and class1 is None:
            cleaned_data['class_slot_1'] = class2
            cleaned_data['class_slot_2'] = None
            self.class_slot_1 = class2
            self.class_slot_2 = None

        if race2 is not None and race1 is None:
            cleaned_data['race_slot_1'] = race2
            cleaned_data['race_slot_2'] = None

        return cleaned_data


class GamerOrderForm(GamerForm):
    class Meta(GamerForm.Meta):
        model = Gamer
        fields = GamerForm.Meta.fields + ['order']
    order = forms.IntegerField(label=_('Order'), initial=1, min_value=1, required=False)

    def clean(self):
        cleaned_data = super(GamerOrderForm, self).clean()
        order = self.cleaned_data['order']

        gamers = self.instance.game.gamers.all()
        error = False
        for gamer in gamers:
            if gamer.id is not self.instance.id and order is not None and gamer.order == order:
                error = True
        if error is True:
            raise forms.ValidationError(_('This order has already been taken :('))
        return cleaned_data


class GamerEditForm(GamerForm):
    class Meta(GamerForm.Meta):
        model = Gamer

    def __init__(self, *args, **kwargs):
        super(GamerEditForm, self).__init__(*args, **kwargs)
        self.fields.pop('status')


class JoinForm(forms.Form):

    nick = forms.CharField(label=_('Nick'))                    # Text input for player's nickname
    game_pass = forms.CharField(label=_('Game access code'))   # Text input for game password

    #def __init__(self, user):
    #    self.user = user

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


class EditGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'max_players', 'winning_level']
    name = forms.CharField(label=_("Name"))
    max_players = forms.IntegerField(label=_("Players number"), min_value=2, max_value=8, initial=6)
    winning_level = forms.IntegerField(label=_("Finish at level"), min_value=1, initial=10)
