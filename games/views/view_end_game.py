from django.views import generic
from games.models.model_game import Game


class EndGameView(generic.DetailView):
    model = Game
    template_name = 'games/game_end.html'

    def get_queryset(self):
        return Game.objects
