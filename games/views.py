from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views import generic
from django.urls import reverse, reverse_lazy
from .models import Game, Gamer, CharacterRace, CharacterClass, GENDER_CHOICES
from django import forms
import random
import string
# from django.http import JsonResponse


def redirect(request):
    gamer_id = request.session.get('gamer_id', None)
    if gamer_id is not None:
        return HttpResponseRedirect(reverse('games:gamer', args=(gamer_id,)))
    return super(GameAccessView, self).dispatch(request, *args, **kwargs)


class GamerForm(forms.ModelForm):
    class Meta:
        model = Gamer
        fields = ['level', 'bonus', 'gender', 'race_slot_1', 'race_slot_2', 'class_slot_1', 'class_slot_2']
    level = forms.IntegerField(label='Level', initial=1, min_value=1)
    bonus = forms.IntegerField(label='Bonus', initial=0)
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    race_slot_1 = forms.ModelChoiceField(queryset=CharacterRace.objects.all(), required=False)
    race_slot_2 = forms.ModelChoiceField(queryset=CharacterRace.objects.all(), required=False)
    class_slot_1 = forms.ModelChoiceField(queryset=CharacterClass.objects.all(), required=False)
    class_slot_2 = forms.ModelChoiceField(queryset=CharacterClass.objects.all(), required=False)


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

        '''
        gamer_id = request.session.get('gamer_id', None)
        if gamer_id is not None:
            if self.get_object().id != gamer_id:
                raise Http404("No gamer found matching the query")
        else:
            return HttpResponseRedirect(reverse('games:game_access'))
        '''
        return super(GamerView, self).dispatch(request, *args, **kwargs)

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


'''
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'home.html',
        context={
            'num_visits': num_visits},  # num_visits appended
    )
'''


class GameAccessView(generic.FormView):                     # GUI for joining existing game
    template_name = 'games/game_access.html'
    form_class = JoinForm

    '''
    def dispatch(self, request, *args, **kwargs):
        # redirect(request)
        gamer_id = request.session.get('gamer_id', None)
        if gamer_id is not None:
            return HttpResponseRedirect(reverse('games:gamer', args=(gamer_id,)))
        return super(GameAccessView, self).dispatch(request, *args, **kwargs)
    '''

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
                # request.session.get('gamer_id', gamer.id)
                # request.session['gamer_id']
                request.session['gamer_id'] = gamer.id          # Add gamer id to actual session
                if request.user.is_authenticated:
                    gamer.user = request.user
                gamer.save()
            else:
                return HttpResponse('Sorry, this game has already finished.')
        else:
            return HttpResponse('Sorry, no more places available. :-(')

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
    # success_url =

    def form_valid(self, form):
        form.instance.host = self.request.user
        form.instance.game_code = generate_game_code()
        form.save()
#        return HttpResponse("Game created yo!")     # super(CreateGameView, self).form_valid(form)
        return HttpResponseRedirect(reverse('games:game_panel', args=(form.instance.id,)))

class EditGameView(generic.UpdateView):
    model = Game
    fields = ['name', 'max_players', 'winning_level']
    template_name = 'games/game_edit.html'
    # success_url =

    def get_queryset(self):
        return Game.objects

    def form_valid(self, form):
        form.save()
#        return HttpResponse("Game edited yo!")      # super(CreateGameView, self).form_valid(form)
        return HttpResponseRedirect(reverse('games:game_panel', args=(form.instance.id,)))

class DeleteGamer(generic.DeleteView):
    model = Gamer
    template_name = 'games/delete_gamer.html'
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        request.session['gamer_id'] = None
        # request.session.modified = True
        return super(DeleteGamer, self).delete(request, *args, **kwargs)


"""
def update_stats(request, gamer_id):
    gamer = get_object_or_404(Gamer, pk=gamer_id)

    gamer.level = request.POST['level']

    gamer.bonus = request.POST['bonus']

    gamer.gender = request.POST['gender']

    gamer.save()

    return HttpResponseRedirect(reverse('games:gamer', args=(gamer_id,)))
"""
"""

class GamePanelView(generic.DetailView):
    template_name = 'games/game_panel.html'
    model = Game

    def get_queryset(self):
        return Game.objects
"""


def game_panel_view(request, pk):
        game = Game.objects.get(pk=pk)
        gamers = Gamer.objects.filter(game__game_code=game.game_code).order_by('id')
        context = {'gamers': gamers, 'game': game}

        return render(request, 'games/game_panel.html', context)
