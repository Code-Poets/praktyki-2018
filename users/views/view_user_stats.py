from django.views import generic
from users.models import CustomUser
from games.models.model_game import Game
from games.models.model_gamer import Gamer
from django.db.models import Q
from django.http import Http404
#from django.contrib import messages
from django.utils.translation import gettext as _


NO_USER_FOUND_MESSAGE = "No user found"


class UserStats(generic.DetailView):
    model = CustomUser
    template_name = 'users/user_stats.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            raise Http404(NO_USER_FOUND_MESSAGE)
        else:
            if self.get_object() != self.request.user:
                raise Http404(NO_USER_FOUND_MESSAGE)
        return super(UserStats, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(UserStats, self).get_context_data(**kwargs)
        data['hosted_games'] = Game.objects.filter(host=self.request.user, finished_at=None)
        data['hosted_end_games'] = Game.objects.filter(host=self.request.user).filter(~Q(finished_at=None))
        data['gamers'] = Gamer.objects.filter(user=self.request.user, game__finished_at=None)
        data['gamers_end'] = Gamer.objects.filter(user=self.request.user).filter(~Q(game__finished_at=None))
        return data
