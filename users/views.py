from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import redirect

from .forms import CustomUserCreationForm
from .models import CustomUser
from games.models import Game, Gamer
from django.db.models import Q


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super(SignUp, self).dispatch(request, *args, **kwargs)


class UserStats(generic.DetailView):
    model = CustomUser
    template_name = 'users/user_stats.html'

    def get_queryset(self):
        return CustomUser.objects

    def get_context_data(self, **kwargs):
        data = super(UserStats, self).get_context_data(**kwargs)
        data['hosted_games'] = Game.objects.filter(host=self.request.user, finished_at=None)
        data['hosted_end_games'] = Game.objects.filter(host=self.request.user).filter(~Q(finished_at=None))
        data['gamers'] = Gamer.objects.filter(user=self.request.user, game__finished_at=None)
        data['gamers_end'] = Gamer.objects.filter(user=self.request.user).filter(~Q(game__finished_at=None))
        return data

