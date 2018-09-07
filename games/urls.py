from django.urls import path

from .views import view_encyclopedia
from .views import view_create_game
from .views import view_delete_gamer
from .views import view_edit_game
from .views import view_edit_gamer_order
from .views import view_edit_gamer
from .views import view_end_game
from .views import view_game_access
from .views import view_game_panel
from .views import view_gamer
from .views import view_help
from .views import view_kick_gamer
from .views import view_stats_game
from .views import view_update_stats

#from . import views as views

app_name = 'games'
urlpatterns = [
    # ex: /games/
    # path('', views.IndexView.as_view(), name='index'),
    path('encyclopedia/', view_encyclopedia.encyclopedia_view, name='encyclopedia'),

    # ex: /games/create/
    path('create/', view_create_game.CreateGameView.as_view(), name='create_game'),
    # ex: /games/1
    path('<int:pk>/', view_game_panel.GamePanelView.as_view(), name='game_panel'),
    # ex: /games/1/edit
    path('<int:pk>/edit/', view_edit_game.EditGameView.as_view(), name='edit_game'),
    # ex: /games/1/edit/gamer/order
    path('<int:pk>/edit/gamer/order', view_edit_gamer_order.EditGamerOrderView.as_view(), name='edit_gamer_order'),
    # ex: /games/1/end
    path('<int:pk>/end/', view_end_game.EndGameView.as_view(), name='end_game'),
    # ex: /games/1/edit/gamer/
    path('<int:pk>/edit/gamer/', view_edit_gamer.EditGamerView.as_view(), name='edit_gamer'),
    # ex: /games/1/end/update
    path('<int:pk>/end/update/', view_update_stats.update_stats, name='update_stats'),
    # ex: /games/1/stats
    path('<int:pk>/stats/', view_stats_game.StatsGameView.as_view(), name='game_stats'),

    # ex: /games/access/
    path('access/', view_game_access.GameAccessView.as_view(), name='game_access'),
    # ex: /games/ABCD/Humbert/join_game/
    # path('<gamepass>/<nick>/join_game/', views.join_game, name='join_game'),
    # ex: /games/gamer/5/
    path('gamer/<int:pk>/', view_gamer.GamerView.as_view(), name='gamer'),
    # ex: /games/gamer/5/lave
    path('gamer/<int:pk>/leave/', view_delete_gamer.DeleteGamerView.as_view(), name='delete_gamer'),
    # ex: /games/gamer/5/kick
    path('gamer/<int:pk>/kick/', view_kick_gamer.KickGamerView.as_view(), name='kick_gamer'),
    # ex: /games/help/
    path('help/', view_help.help_view, name='help')
]
