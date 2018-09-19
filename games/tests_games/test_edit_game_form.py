from django.test import TestCase
from games.forms import EditGameForm
from games.models import Game, MAX_GAMERS_PER_GAME, MIN_GAMERS_PER_GAME, MIN_WINNING_LEVEL


class EditGameFormTests(TestCase):
    def test_max_players(self):
        form=EditGameForm(data={
            'name': 'Name',
            'max_players': MAX_GAMERS_PER_GAME,
            'winning_level': MIN_WINNING_LEVEL,
        })
        self.assertTrue(form.is_valid())

    def test_min_players(self):
        form=EditGameForm(data={
            'name': 'Name',
            'max_players': MIN_GAMERS_PER_GAME,
            'winning_level': MIN_WINNING_LEVEL,
        })
        self.assertTrue(form.is_valid())

    def test_blank_name(self):
        form=EditGameForm(data={
            'name': None,
            'max_players': MAX_GAMERS_PER_GAME,
            'winning_level': MIN_WINNING_LEVEL,
        })
        self.assertFalse(form.is_valid())

    def test_too_low_max_players(self):
        form=EditGameForm(data={
            'name': 'Name',
            'max_players': MIN_GAMERS_PER_GAME-1,
            'winning_level': MIN_WINNING_LEVEL,
        })
        self.assertFalse(form.is_valid())

    def test_too_high_max_players(self):
        form=EditGameForm(data={
            'name': 'Name',
            'max_players': MAX_GAMERS_PER_GAME+1,
            'winning_level': MIN_WINNING_LEVEL,
        })
        self.assertFalse(form.is_valid())

    def test_blank_max_players(self):
        form=EditGameForm(data={
            'name': 'Name',
            'max_players': None,
            'winning_level': MIN_WINNING_LEVEL,
        })
        self.assertFalse(form.is_valid())

    def test_invalid_winning_level(self):
        form=EditGameForm(data={
            'name': 'Name',
            'max_players': MAX_GAMERS_PER_GAME,
            'winning_level': MIN_WINNING_LEVEL-1,
        })
        self.assertFalse(form.is_valid())

    def test_blank_winning_level(self):
        form=EditGameForm(data={
            'name': 'Name',
            'max_players': MAX_GAMERS_PER_GAME,
            'winning_level': None,
        })
        self.assertFalse(form.is_valid())
