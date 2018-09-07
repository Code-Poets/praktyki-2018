from django.shortcuts import render

def help_view(request):
    return render(request, 'games/instruction_manual.html')
