from django.test import TestCase
from django.urls import reverse
from games.models import Game, CustomUser, Gamer


class GamePanel(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'nobodyuser',
            'password': 'nobodypassword'
        }
        self.host = CustomUser.objects.create_user(**self.credentials)

        self.credentials = {
            'host': self.host,
            'game_code': 'XXXX',
            'name': 'NewGameTest',
            'max_players': 3,
            'winning_level': 10
        }
        self.game = Game.objects.create(**self.credentials)

        self.credentials = {
            'nick': 'gamer1',
            'game': self.game,
            # 'level': '10'
        }
        self.gamer1 = Gamer.objects.create(**self.credentials)

        self.credentials = {
            'nick': 'gamer2',
            'game': self.game,
            # 'level': '10'
        }
        self.gamer2 = Gamer.objects.create(**self.credentials)

        self.credentials = {
            'nick': 'gamer3',
            'game': self.game,
            # 'level': '10'
        }
        self.gamer3 = Gamer.objects.create(**self.credentials)

        self.credentials = {
            'nick': 'gamer4',
            'game': self.game,
            'level': '10'
        }
        self.gamer4 = Gamer.objects.create(**self.credentials)

    def test_full_room(self):
        url = reverse('games:game_panel', args=(self.game.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/game_panel.html')
        self.assertContains(response, '<b> NewGameTest </b>')
        self.assertContains(response, 'gamer1')
        # self.assertIs(self.game, False)
