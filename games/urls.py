from django.urls import path

from . import views

app_name = 'games'
urlpatterns = [
    # path('', views.IndexView.as_view(), name='index'),
    path('gamer/<int:pk>', views.GamerView.as_view(), name='gamer'),
    path('access/', views.GameAccessView.as_view(), name='game_access'),
    path('<gamepass>/<nick>/join_game/', views.join_game, name='join_game'),
    path('create/', views.CreateGameView.as_view(), name='create_game'),
    path('<int:pk>/edit/', views.EditGameView.as_view(), name='edit_game'),
    path('gamer/<int:pk>/leave', views.DeleteGamer.as_view(), name='delete_gamer'),
    # path('gamer/<int:gamer_id>/update', views.update_stats, name='update_stats'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<int:pk>/', views.game_panel_view, name='game_panel'),
]
