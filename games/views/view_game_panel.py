from django.views import generic
from games.models import Game, Gamer


class GamePanelView(generic.DetailView):
    model = Game
    template_name = 'games/game_panel.html'

    def get_queryset(self):
        return Game.objects

    def get_context_data(self, **kwargs):
        context = super(GamePanelView, self).get_context_data(**kwargs)
        context['game'] = Game.objects.get(pk=self.kwargs['pk'])
        context['gamers'] = Gamer.objects.filter(game__id=self.kwargs['pk']).order_by('order')
        return context
