from django.http import HttpResponseRedirect, Http404
from django.views import generic
from django.urls import reverse
from games.models.model_gamer import Gamer


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
