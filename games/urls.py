from django.urls import path

from . import views

app_name = 'games'
urlpatterns = [
    # ex: /games/
    # path('', views.IndexView.as_view(), name='index'),

    # ex: /games/create/
    path('create/', views.CreateGameView.as_view(), name='create_game'),
    # ex: /games/1
    path('<int:pk>/', views.game_panel_view, name='game_panel'),
    # ex: /games/1/edit
    path('<int:pk>/edit/', views.EditGameView.as_view(), name='edit_game'),
    # ex: /games/1/end
    path('<int:pk>/end/', views.EndGameView.as_view(), name='end_game'),
    # ex: /games/1/end/update
    path('<int:pk>/end/update/', views.update_stats, name='update_stats'),

    # ex: /games/access/
    path('access/', views.GameAccessView.as_view(), name='game_access'),
    # ex: /games/ABCD/Humbert/join_game/
    path('<gamepass>/<nick>/join_game/', views.join_game, name='join_game'),
    # ex: /games/gamer/5/
    path('gamer/<int:pk>', views.GamerView.as_view(), name='gamer'),
    # ex: /games/gamer/5/lave
    path('gamer/<int:pk>/leave', views.DeleteGamer.as_view(), name='delete_gamer'),
]
