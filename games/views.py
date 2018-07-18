from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from .models import Game, Gamer, CharacterRace, CharacterClass
from django import forms
#from django.http import JsonResponse


class GamerForm(forms.ModelForm):
    class Meta:
        model = Gamer
        fields = ['level', 'bonus', 'gender', 'race_slot_1', 'race_slot_2', 'class_slot_1', 'class_slot_2']
    level = forms.IntegerField(label='Level', initial=1)
    bonus = forms.IntegerField(label='Bonus', initial=0)
    race_slot_1 = forms.ModelChoiceField(queryset=CharacterRace.objects.all(), required=False)
    race_slot_2 = forms.ModelChoiceField(queryset=CharacterRace.objects.all(), required=False)
    class_slot_1 = forms.ModelChoiceField(queryset=CharacterClass.objects.all(), required=False)
    class_slot_2 = forms.ModelChoiceField(queryset=CharacterClass.objects.all(), required=False)
    #gender = forms.ChoiceField


"""
class AjaxableResponseMixin:
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response
"""


class GamerView(generic.UpdateView):                        # GUI for player's stats in current game
    model = Gamer
    form_class = GamerForm
    template_name = 'games/gamer.html'

    def get_queryset(self):
        return Gamer.objects

    def form_valid(self, form):
        self.object = form.save()
        return self.render_to_response(self.get_context_data(form=form))


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

    def get_initial(self):

        initial = super(GameAccessView, self).get_initial()

        if self.request.user.is_authenticated:
            initial['nick'] = self.request.user.nick

        return initial

    def form_valid(self, form):                            # Pass nickname and password to join_game view
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        game_pass = form.get_game_pass()
        nick = form.get_nick()
        return HttpResponseRedirect(reverse('games:join_game', args=(game_pass, nick)))


def join_game(request, gamepass, nick):                     # View for assigning player to game
    try:
        game = Game.objects.get(game_code=gamepass)          # Find player by nickname in existing players
    except Game.DoesNotExist:
        return HttpResponse('WHOOPS! No such game could be found!')
    try:
        # from ipdb import set_trace; set_trace()
        gamer = game.gamers.get(nick=nick)                  # Find player by nickname in existing players
        if gamer.user is None or gamer.user.id is not request.user.id:
            return HttpResponse('This nickname has already been taken. :-(')
    except Gamer.DoesNotExist:
        if game.is_available():
            if not game.is_finished():
                gamer = Gamer.objects.create(                   # Create player and add to game if possible
                    game=game,
                    nick=nick
                )
                if request.user.is_authenticated:
                    gamer.user = request.user
                gamer.save()
            else:
                return HttpResponse('Sorry, this game has already finished.')
        else:
            return HttpResponse('Sorry, no more places available. :-(')

    return HttpResponseRedirect(reverse('games:gamer', args=(gamer.id,)))


"""
def update_stats(request, gamer_id):
    gamer = get_object_or_404(Gamer, pk=gamer_id)

    gamer.level = request.POST['level']

    gamer.bonus = request.POST['bonus']

    gamer.gender = request.POST['gender']

    gamer.save()

    return HttpResponseRedirect(reverse('games:gamer', args=(gamer_id,)))
"""


class GamePanelView(generic.DetailView):                     # GUI of all game
    template_name = 'games/game_panel.html'
    model = Game

    def get_queryset(self):
        return Game.objects
