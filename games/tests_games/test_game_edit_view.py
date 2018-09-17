from django.test import TestCase
from django.urls import reverse
from games.models import Game, Gamer, CustomUser


class GameEditViewTests(TestCase):
    def setUp(self):

        user1 = CustomUser.objects.create_user(
            username='nobodyuser2',
            email='email2',
            nick='SammyClassicSonicFan'
        )
        user1.set_password('nobodypassword')
        user1.save()

        user2 = CustomUser.objects.create_user(
            username='nobodyuser3',
            email='email3',
            nick='IH8MarsBars'
        )
        user2.set_password('nobodypassword')
        user2.save()

        self.user=user1

        self.game_name = 'Game'
        self.game_players = 6
        self.game_level = 10

        self.game = Game.objects.create(
            host=user1,
            game_code='XXXX',
            name=self.game_name,
            max_players=self.game_players,
            winning_level=self.game_level
        )

        other_game = Game.objects.create(
            host=user1,
            game_code='YYYY',
            name='OtherGame',
            max_players=2,
            winning_level=10,
        )

        yet_another_game = Game.objects.create(
            host=user2,
            game_code='ZZZZ',
            name='YetAnotherGame',
            max_players=2,
            winning_level=10,
        )

        self.correct_gamer_1='game_gamer1'
        self.correct_gamer_2='game_gamer2'
        self.incorrect_gamer_1='other_game_gamer1'
        self.incorrect_gamer_2='other_game_gamer2'
        self.incorrect_gamer_3='yet_another_game_gamer1'
        self.incorrect_gamer_4='yet_another_game_gamer2'


        game_gamer1 = Gamer.objects.create(  # Create player and add to game if possible
            game=self.game,
            user=user1,
            nick=self.correct_gamer_1
        )

        game_gamer2 = Gamer.objects.create(  # Create player and add to game if possible
            game=self.game,
            user=user2,
            nick=self.correct_gamer_2
        )

        other_game_gamer1 = Gamer.objects.create(  # Create player and add to game if possible
            game=other_game,
            user=user1,
            nick=self.incorrect_gamer_1
        )

        other_game_gamer2 = Gamer.objects.create(  # Create player and add to game if possible
            game=other_game,
            user=user2,
            nick=self.incorrect_gamer_2
        )

        yet_another_game_gamer1 = Gamer.objects.create(  # Create player and add to game if possible
            game=yet_another_game,
            user=user1,
            nick=self.incorrect_gamer_3
        )

        yet_another_game_gamer2 = Gamer.objects.create(  # Create player and add to game if possible
            game=yet_another_game,
            user=user2,
            nick=self.incorrect_gamer_4
        )

        self.url = reverse('games:edit_game', args=(self.game.id,))
        self.template_name = 'games/game_edit.html'

    def test_gamer_list_display(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.template_name)
        self.assertContains(response, self.correct_gamer_1)
        self.assertContains(response, self.correct_gamer_2)
        self.assertNotContains(response, self.incorrect_gamer_1)
        self.assertNotContains(response, self.incorrect_gamer_2)
        self.assertNotContains(response, self.incorrect_gamer_3)
        self.assertNotContains(response, self.incorrect_gamer_4)

    def test_game_editing_name(self):
        self.client.force_login(self.user)
        new_name = 'NewName'
        response = self.client.post(self.url, {'name': new_name, 'max_players': self.game_players, 'winning_level': self.game_level})
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(self.template_name)
        #self.assertEqual(self.game.name, new_name)

    def test_game_editing_players(self):
        self.client.force_login(self.user)
        new_players = 8
        response = self.client.post(self.url, {'name': self.game_name, 'max_players': new_players, 'winning_level': self.game_level})
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(self.template_name)
        #self.assertEqual(self.game.max_players, new_players)

    def test_game_editing_level(self):
        self.client.force_login(self.user)
        new_level = 12
        response = self.client.post(self.url, {'name': self.game_name, 'max_players': self.game_players, 'winning_level': new_level})
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(self.template_name)
        #self.assertEqual(self.game.max_players, new_level)
