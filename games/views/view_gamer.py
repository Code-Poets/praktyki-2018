from django.http import HttpResponseRedirect, Http404
from django.views import generic
from django.urls import reverse
from games.models import Game, Gamer, CharacterRace, CharacterClass, GENDER_CHOICES
# from django.http import JsonResponse
from games.forms.form_gamer import GamerForm


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
                    raise Http404("No cookie found")
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
