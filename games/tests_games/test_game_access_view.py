from django.test import TestCase
from django.urls import reverse
from games.models.model_game import Game
from games.models.model_gamer import Gamer
from users.models import CustomUser
from django.utils import timezone

# Create your tests here.


class GameAccessViewTests(TestCase):
    def setUp(self):
        self.url = reverse('games:game_access')

        user1 = CustomUser.objects.create_user(
            username='nobodyuser',
            email='email1',
            nick='DogmaSlayer666'
        )
        user1.set_password('nobodypassword')
        user1.save()

        user2 = CustomUser.objects.create_user(
            username='nobodyuser2',
            email='email2',
            nick='SammyClassicSonicFan'
        )
        user2.set_password('nobodypassword')
        user2.save()

        user3 = CustomUser.objects.create_user(
            username='nobodyuser3',
            email='email3',
            nick='IH8MarsBars'
        )
        user3.set_password('nobodypassword')
        user3.save()

        self.user1=user1
        self.user2=user2
        self.user3=user3

        self.game = Game.objects.create(
            host=self.user1,
            game_code='XXXX',
            name='NewGameTest',
            max_players=2,
            winning_level=10
        )

        self.full_game = Game.objects.create(
            host=self.user1,
            game_code='XXYY',
            name='FullGameTest',
            max_players=2,
            winning_level=10
        )

        self.finished_game = Game.objects.create(
            host=self.user1,
            game_code='YYYY',
            name='FinishedGameTest',
            max_players=2,
            winning_level=10,
            finished_at=timezone.now() - timezone.timedelta(days=1)
        )

        game_gamer1 = Gamer.objects.create(  # Create player and add to game if possible
            game=self.game,
            user=self.user1,
            nick=self.user1.nick
        )

        full_game_gamer1 = Gamer.objects.create(  # Create player and add to game if possible
            game=self.full_game,
            user=self.user1,
            nick=self.user1.nick
        )

        full_game_gamer2 = Gamer.objects.create(  # Create player and add to game if possible
            game=self.full_game,
            user=self.user2,
            nick=self.user2.nick
        )

    def test_unregistered_bad_code(self):
        response = self.client.post(self.url, {'nick': 'nickname', 'game_pass': 'ZZZZ'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/game_access.html')
        self.assertContains(response, 'WHOOPS! No such game could be found!')

    def test_unregistered_joining(self):
        response = self.client.post(self.url, {'nick': 'nickname', 'game_pass': self.game.game_code})
        self.assertEqual(response.status_code, 302)
        #self.assertRedirect(response, 'games/game_access.html')

    def test_unregistered_taken_nickname(self):
        response = self.client.post(self.url, {'nick': self.user1.nick, 'game_pass': self.game.game_code})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/game_access.html')
        self.assertContains(response, 'This nickname has already been taken. :-(')

    #def test_unregistered_rejoining(self):

    def test_registered_bad_code(self):
        self.client.force_login(self.user2)
        response = self.client.post(self.url, {'nick': self.user2.nick, 'game_pass': 'ZZZZ'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/game_access.html')
        self.assertContains(response, 'WHOOPS! No such game could be found!')

    def test_registered_taken_nickname(self):
        self.client.force_login(self.user2)
        response = self.client.post(self.url, {'nick': self.user1.nick, 'game_pass': self.game.game_code})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/game_access.html')
        self.assertContains(response, 'This nickname has already been taken. :-(')

    def test_registered_joining(self):
        self.client.force_login(self.user2)
        #self.assertTrue(login)
        response = self.client.post(self.url, {'nick': self.user2.nick, 'game_pass': self.game.game_code})
        self.assertEqual(response.status_code, 302)

    def test_registered_rejoining(self):
        self.client.force_login(self.user1) #login(username=self.user1.username, password=self.user1.password)
        response = self.client.post(self.url, {'nick': self.user1.nick, 'game_pass': self.game.game_code})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/game_access.html')
        self.assertContains(response, 'You have already joined this game!')

    def test_unregistered_game_full(self):
        response = self.client.post(self.url, {'nick': 'nickname', 'game_pass': self.full_game.game_code})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/game_access.html')
        self.assertContains(response, 'Sorry, no more places available. :-(')

    def test_unregistered_game_finished(self):
        response = self.client.post(self.url, {'nick': 'nickname', 'game_pass': self.finished_game.game_code})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/game_access.html')
        self.assertContains(response, 'Sorry, this game has already finished.')

    def test_registered_game_full(self):
        self.client.force_login(self.user3)
        response = self.client.post(self.url, {'nick': self.user3.nick, 'game_pass': self.full_game.game_code})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/game_access.html')
        self.assertContains(response, 'Sorry, no more places available. :-(')

    def test_registered_game_finished(self):
        self.client.force_login(self.user1)
        response = self.client.post(self.url, {'nick': self.user1.nick, 'game_pass': self.finished_game.game_code})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/game_access.html')
        self.assertContains(response, 'Sorry, this game has already finished.')
