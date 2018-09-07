from django.shortcuts import render
from games.models import CharacterRace, CharacterClass

def encyclopedia_view(request):
        list_race = CharacterRace.objects.all()
        list_class = CharacterClass.objects.all()
        path = request.path
        context = {'list_race': list_race, 'list_class': list_class, 'path': path}

        return render(request, 'games/encyclopedia.html', context)
