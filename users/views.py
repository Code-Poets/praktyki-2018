from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import redirect
from .forms import CustomUserCreationForm
from .models import CustomUser
from games.models import Game, Gamer
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render


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

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            raise Http404("No user found")
        else:
            if self.get_object() != self.request.user:
                raise Http404("No user found")
        return super(UserStats, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return CustomUser.objects

    def get_context_data(self, **kwargs):
        data = super(UserStats, self).get_context_data(**kwargs)
        data['hosted_games'] = Game.objects.filter(host=self.request.user, finished_at=None)
        data['hosted_end_games'] = Game.objects.filter(host=self.request.user).filter(~Q(finished_at=None))
        data['gamers'] = Gamer.objects.filter(user=self.request.user, game__finished_at=None)
        data['gamers_end'] = Gamer.objects.filter(user=self.request.user).filter(~Q(game__finished_at=None))
        return data


class DeleteUserView(generic.DeleteView):
    model = CustomUser
    template_name = 'users/delete_user.html'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            raise Http404("No user found")
        else:
            if self.get_object() != self.request.user:
                raise Http404("No user found")
        return super(DeleteUserView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        request.session['user_id'] = None
        return super(DeleteUserView, self).delete(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return HttpResponseRedirect(reverse('change_password'))
        else:
            return super(DeleteUserView, self).post(request, *args, **kwargs)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {
        'form': form
    })
