from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from games.models.model_game import Game
import random
import string
from games.forms.form_edit_game import EditGameForm


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

class CreateGameView(generic.CreateView):
    model = Game
    #fields = ['name', 'max_players', 'winning_level']
    template_name = 'games/game_create.html'
    form_class = EditGameForm

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
