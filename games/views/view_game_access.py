from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from games.models.model_game import Game
from games.models.model_gamer import Gamer
from games.forms.form_join import JoinForm


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
            initial['gamer_id'] = self.request.session['gamer_id']

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

        for x in range(1, game.max_players+1):
            try:
                gamegamer = Gamer.objects.get(game__game_code=game_pass, order=x)
            except Gamer.DoesNotExist:
                gamegamer = None
                gamer.order = x
                break
        self.request.session['gamer_id'] = gamer.id  # Add gamer id to actual session
        if self.request.user.is_authenticated:
            gamer.user = self.request.user
        gamer.save()

        return HttpResponseRedirect(reverse('games:gamer', args=(gamer.id,)))
