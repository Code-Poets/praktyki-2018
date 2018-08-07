from django.test import TestCase
from django.urls import reverse
from games.models import Game, CustomUser

# Create your tests here.


class GamePanel(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'nobodyuser',
            'password': 'nobodypassword'}
        gamer = CustomUser.objects.create_user(**self.credentials)

        self.credentials = {
            'host': gamer,
            'game_code': 'XXXX',
            'name': 'NewGameTest',
            'max_players': 6,
            'winning_level': 10}
        self.game = Game.objects.create(**self.credentials)

    def test_index_page(self):
        url = reverse('games:game_panel', args=(self.game.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/game_panel.html')
        self.assertContains(response, 'Welcome to: </font>NewGameTest')
