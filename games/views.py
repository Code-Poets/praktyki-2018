from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django import forms
from .models import Game, Gamer
from django import forms


# Create your views here.
class GamerView(generic.DetailView):
    model = Gamer
    template_name = 'games/gamer.html'

    def get_queryset(self):
        return Gamer.objects


class JoinForm(forms.Form):
    nick = forms.CharField(label='Nick')
    game_pass = forms.CharField(label='Game access code')

    def get_game_pass(self):
        return self.data['game_pass']

    def get_nick(self):
        return self.data['nick']


#def game_access(request):
#    return render(request, 'games/game_access.html')


class GameAccessView(generic.FormView):
    template_name = 'games/game_access.html'
    form_class = JoinForm
    #success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        #return super().form_valid(form)
        game_pass = form.get_game_pass()
        nick = form.get_nick()
        return HttpResponseRedirect(reverse('games:join_game', args=(game_pass, nick)))


def join_game(request, gamepass, nick):
    #game = get_object_or_404(Game, password=gamepass)

    #gamer_id = None
    #return HttpResponseRedirect('games/gamer.html', gamer_id)
    return HttpResponse('Redirect succesful')


def update_stats(request, gamer_id):
    return HttpResponseRedirect('games/gamer.html', gamer_id)