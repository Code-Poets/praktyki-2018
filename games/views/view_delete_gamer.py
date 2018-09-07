from django.http import HttpResponseRedirect, Http404
from django.views import generic
from django.urls import reverse
from games.models import Gamer


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
