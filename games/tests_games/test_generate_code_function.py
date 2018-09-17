from django.test import TestCase
from games.views import generate_game_code
from games.models import GAME_CODE_LENGTH


class GenerateGameCodeTests(TestCase):
    #def setUp(self):

    def test_code_is_generated(self):
        game_code = generate_game_code()
        self.assertEqual(len(game_code), GAME_CODE_LENGTH)

    #def test_code_is_unique(self):
