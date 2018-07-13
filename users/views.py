from django.urls import reverse_lazy
from django.views import generic

from .forms import CustomUserCreationForm


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class JoinIn(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'join_game.html'


class Create(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'create_game.html'
