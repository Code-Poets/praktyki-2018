from django.http import HttpResponseRedirect, Http404
from django.views import generic
from django.urls import reverse
from games.models import Game, Gamer
from games.forms.form_edit_game import EditGameForm


class EditGameView(generic.UpdateView):
    #model = Game
    #fields = ['name', 'max_players', 'winning_level']
    template_name = 'games/game_edit.html'
    form_class = EditGameForm

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
                raise Http404("No game found")
        else:
            if self.get_object().host != self.request.user:
                raise Http404("No game found")
        return super(EditGameView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Game.objects

    def get_context_data(self, **kwargs):
        context = super(EditGameView, self).get_context_data(**kwargs)
        context['gamers'] = Gamer.objects.filter(game__id=self.kwargs['pk']).order_by('order')
        return context

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('games:edit_game', args=(form.instance.id,)))
