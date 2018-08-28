from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views import generic
from django.urls import reverse, reverse_lazy
from .models import Game, Gamer, CharacterRace, CharacterClass, GENDER_CHOICES
from django import forms
import random
import string
from django.utils import timezone
# from django.http import JsonResponse


class GamerForm(forms.ModelForm):
    class Meta:
        model = Gamer
        fields = ['status', 'level', 'bonus', 'gender', 'race_slot_1', 'race_slot_2', 'class_slot_1', 'class_slot_2', 'order']
    status = forms.CharField(label='Status', required=False)
    level = forms.IntegerField(label='Level', initial=1, min_value=1)
    bonus = forms.IntegerField(label='Bonus', initial=0)
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    race_slot_1 = forms.ModelChoiceField(queryset=CharacterRace.objects.all(), required=False, label='Race')
    race_slot_2 = forms.ModelChoiceField(queryset=CharacterRace.objects.all(), required=False)
    class_slot_1 = forms.ModelChoiceField(queryset=CharacterClass.objects.all(), required=False, label='Class')
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

    order = forms.IntegerField(label='Order', initial=1, min_value=1)


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

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().game.finished_at is not None:
            raise Http404("Game is finished")
        else:
            if self.request.user.is_authenticated:
                if self.get_object().user != self.request.user:
                    raise Http404("Gamer not belong to this user")
            else:
                # if 'gamer_id' not in request.session:
                gamer_id = request.session.get('gamer_id', None)
                if gamer_id is None:
                    raise Http404("No cookie fond")
                else:
                    # gamer_id = request.session['gamer_id']
                    if self.get_object().id != request.session['gamer_id']:
                        raise Http404("Cookie for other gamer")

        return super(GamerView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Gamer.objects

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(reverse('games:gamer', args=(self.get_object().id,)))


class JoinForm(forms.Form):

    nick = forms.CharField(label='Nick')                    # Text input for player's nickname
    game_pass = forms.CharField(label='Game access code')   # Text input for game password

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
            raise forms.ValidationError('WHOOPS! No such game could be found!')

        if user is not None:
            logged_gamer = Gamer.objects.filter(game=game, user=user)

            if logged_gamer:
                raise forms.ValidationError('You have already joined this game!')

        if game.is_finished():
            raise forms.ValidationError('Sorry, this game has already finished.')
        if not game.is_available():
            raise forms.ValidationError('Sorry, no more places available. :-(')

        gamers = game.gamers.all()

        for gamer in gamers:
            if gamer.nick == nick:
                raise forms.ValidationError('This nickname has already been taken. :-(')
        return cleaned_data


class GameAccessView(generic.FormView):                     # GUI for joining existing game
    template_name = 'games/game_access.html'
    form_class = JoinForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            data['gamers'] = Gamer.objects.filter(user=self.request.user)

        gamer_cookie = self.request.session.get('gamer_id', None)                 # COOKIE USED
        if gamer_cookie is not None:
            try:
                data['unregistered_gamer'] = Gamer.objects.get(pk=gamer_cookie)
            except Gamer.DoesNotExist:
                self.request.session['gamer_id'] = None
                gamer_cookie = None
        data['gamer_cookie'] = gamer_cookie
        return data

    def get_initial(self):
        initial = super(GameAccessView, self).get_initial()
        if self.request.user.is_authenticated:
            initial['nick'] = self.request.user.nick
            initial['user'] = self.request.user.id
        else:
            initial['user'] = None

        return initial

    def form_valid(self, form):                            # Pass nickname and password to join_game view
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        game_pass = form.get_game_pass()
        nick = form.get_nick()

        game = Game.objects.get(game_code=game_pass)

        gamer = Gamer.objects.create(  # Create player and add to game if possible
            game=game,
            nick=nick
        )
        gamer.order = gamer.id % 8 + 1
        self.request.session['gamer_id'] = gamer.id  # Add gamer id to actual session
        if self.request.user.is_authenticated:
            gamer.user = self.request.user
        gamer.save()

        return HttpResponseRedirect(reverse('games:gamer', args=(gamer.id,)))


def generate_game_code():

    code = ''

    already_exists = True

    unique = True

    while already_exists:
        code = code.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(Game._meta.get_field('game_code').max_length))

        for game in Game.objects.all():
            if game.game_code == code:
                unique = False

        already_exists = not unique

    return code


class EditGameForm(forms.Form):
    name = forms.CharField(label="Name")
    max_players = forms.IntegerField(label="Players number", min_value=2, max_value=8, initial=6)
    winning_level = forms.IntegerField(label="Finish at level", min_value=1, initial=10)


class CreateGameView(generic.CreateView):
    model = Game
    fields = ['name', 'max_players', 'winning_level']
    template_name = 'games/game_create.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        return super(CreateGameView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(CreateGameView, self).get_context_data(**kwargs)
        data['hosted_games'] = Game.objects.filter(host=self.request.user, finished_at=None)
        return data

    def form_valid(self, form):
        form.instance.host = self.request.user
        form.instance.game_code = generate_game_code()
        form.save()
        return HttpResponseRedirect(reverse('games:game_panel', args=(form.instance.id,)))


class EditGameView(generic.UpdateView):
    model = Game
    fields = ['name', 'max_players', 'winning_level']
    template_name = 'games/game_edit.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
                raise Http404("No game found")
        else:
            if self.get_object().host != self.request.user:
                raise Http404("No game found")
        return super(EditGameView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Game.objects

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('games:game_panel', args=(form.instance.id,)))


class EditGamerOrderView(generic.UpdateView):
    model = Gamer
    fields = ['order']
    template_name = 'games/gamer_edit.html'

    def get_queryset(self):
        return Gamer.objects

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('games:edit_game', args=(form.instance.game.id,)))


class DeleteGamerView(generic.DeleteView):
    model = Gamer
    template_name = 'games/delete_gamer.html'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().game.finished_at is not None:
            raise Http404("No gamer found")
        else:
            if self.request.user.is_authenticated:
                if self.get_object().user != self.request.user:
                    raise Http404("No gamer found")
            else:
                # if 'gamer_id' not in request.session:
                gamer_id = request.session.get('gamer_id', None)
                if gamer_id is None:
                    raise Http404("No gamer found")
                else:
                    # gamer_id = request.session['gamer_id']
                    if self.get_object().id != request.session['gamer_id']:
                        raise Http404("No gamer found")
        return super(DeleteGamerView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        request.session['gamer_id'] = None
        return super(DeleteGamerView, self).delete(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return HttpResponseRedirect(reverse('games:gamer', args=(self.get_object().id,)))
        else:
            return super(DeleteGamerView, self).post(request, *args, **kwargs)


class KickGamerView(generic.DeleteView):
    model = Gamer
    template_name = 'games/kick_gamer.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            raise Http404("No gamer found")
        else:
            if self.get_object().game.host != self.request.user:
                raise Http404("No gamer found")
        return super(KickGamerView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.success_url = reverse('games:edit_game', args=(self.object.game.id,))
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return HttpResponseRedirect(reverse('games:edit_game', args=(self.get_object().game.id,)))
        else:
            return super(KickGamerView, self).post(request, *args, **kwargs)


"""

class GamePanelView(generic.DetailView):
    template_name = 'games/game_panel.html'
    model = Game

    def get_queryset(self):
        return Game.objects
"""


def game_panel_view(request, pk):
        game = Game.objects.get(pk=pk)
        gamers = Gamer.objects.filter(game__game_code=game.game_code)
        context = {'gamers': gamers, 'game': game}

        return render(request, 'games/game_panel.html', context)


class EndGameView(generic.DetailView):
    model = Game
    template_name = 'games/game_end.html'

    def get_queryset(self):
        return Game.objects


class EditGamerView(generic.UpdateView):
    model = Gamer
    fields = ['level', 'bonus']
    template_name = 'games/gamer_edit.html'

    def get_queryset(self):
        return Gamer.objects

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('games:end_game', args=(form.instance.game.id,)))


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


class StatsGameView(generic.DetailView):
    model = Game
    template_name = 'games/game_stats.html'

    def get_queryset(self):
        return Game.objects


def encyclopedia_view(request):
        list_race = CharacterRace.objects.all()
        list_class = CharacterClass.objects.all()
        path = request.path
        context = {'list_race': list_race, 'list_class': list_class, 'path': path}

        return render(request, 'games/encyclopedia.html', context)


def help_view(request):
    return render(request, 'games/instruction_manual.html')
