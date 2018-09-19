from django.test import TestCase
from django.urls import reverse
from games.models.model_game import Game
from users.models import CustomUser


class CreateGameViewTests(TestCase):
    def setUp(self):
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

        self.user=user1

        self.game_1_name = 'User1TestGame'
        self.game_2_name = 'User2TestGame'

        game1 = Game.objects.create(
            host=user1,
            game_code='XXXX',
            name=self.game_1_name,
            max_players=2,
            winning_level=10
        )

        game2 = Game.objects.create(
            host=user2,
            game_code='YYYY',
            name=self.game_2_name,
            max_players=2,
            winning_level=10
        )

        self.valid_data = {'name': 'NewGameTest', 'max_players': 6, 'winning_level':10}
        self.url = reverse('games:create_game')
        self.template_name='games/game_create.html'

    def test_current_games_display(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.template_name)
        self.assertContains(response, self.game_1_name)
        self.assertNotContains(response, self.game_2_name)

    def test_game_creation(self):
        self.client.force_login(self.user)
        games_before = Game.objects.filter(host=self.user, finished_at=None).count()
        response = self.client.post(self.url, self.valid_data)
        games_after = Game.objects.filter(host=self.user, finished_at=None).count()
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(self.template_name)
        self.assertEqual(games_before+1, games_after)
