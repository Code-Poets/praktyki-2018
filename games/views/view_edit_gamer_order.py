from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from games.models.model_gamer import Gamer
from games.forms.form_gamer_order import GamerOrderForm


class EditGamerOrderView(generic.UpdateView):
    model = Gamer
    form_class = GamerOrderForm
    template_name = 'games/gamer_edit.html'

    def get_queryset(self):
        return Gamer.objects

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('games:edit_game', args=(form.instance.game.id,)))
