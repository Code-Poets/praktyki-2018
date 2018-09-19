from django.test import TestCase
from django.urls import reverse
from games.models import Game, Gamer, CustomUser, Gender, CharacterRace, CharacterClass


class StatsGameViewTests(TestCase):
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
        self.correct_gamer_3='game_gamer3'
        self.incorrect_gamer_1='other_game_gamer1'
        self.incorrect_gamer_2='other_game_gamer2'
        self.incorrect_gamer_3='other_game_gamer3'
        self.incorrect_gamer_4='yet_another_game_gamer1'
        self.incorrect_gamer_5='yet_another_game_gamer2'
        self.incorrect_gamer_6='yet_another_game_gamer3'


        game_gamer1 = Gamer.objects.create(
            game=self.game,
            user=user1,
            nick=self.correct_gamer_1
        )

        game_gamer2 = Gamer.objects.create(
            game=self.game,
            user=user2,
            nick=self.correct_gamer_2
        )

        game_gamer3 = Gamer.objects.create(
            game=self.game,
            nick=self.correct_gamer_3
        )

        other_game_gamer1 = Gamer.objects.create(
            game=other_game,
            user=user1,
            nick=self.incorrect_gamer_1
        )

        other_game_gamer2 = Gamer.objects.create(
            game=other_game,
            user=user2,
            nick=self.incorrect_gamer_2
        )

        other_game_gamer3 = Gamer.objects.create(
            game=other_game,
            nick=self.incorrect_gamer_3
        )

        yet_another_game_gamer1 = Gamer.objects.create(
            game=yet_another_game,
            user=user1,
            nick=self.incorrect_gamer_4
        )

        yet_another_game_gamer2 = Gamer.objects.create(
            game=yet_another_game,
            user=user2,
            nick=self.incorrect_gamer_5
        )

        yet_another_game_gamer3 = Gamer.objects.create(
            game=yet_another_game,
            user=user2,
            nick=self.incorrect_gamer_6
        )

        self.template_name = 'games/game_end.html'

    def test_gamer_list_display(self):
        response = self.client.get(reverse('games:game_stats', args=(self.game.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.template_name)
        self.assertContains(response, self.game.name)
        self.assertContains(response, self.correct_gamer_1)
        self.assertContains(response, self.correct_gamer_2)
        self.assertContains(response, self.correct_gamer_3)
        self.assertNotContains(response, self.incorrect_gamer_1)
        self.assertNotContains(response, self.incorrect_gamer_2)
        self.assertNotContains(response, self.incorrect_gamer_3)
        self.assertNotContains(response, self.incorrect_gamer_4)
        self.assertNotContains(response, self.incorrect_gamer_5)
        self.assertNotContains(response, self.incorrect_gamer_6)

    def test_gamer_stats_display(self):
        nick='Gamer'
        level=10
        gender=Gender.M.value
        race1=CharacterRace.objects.create(name="race 1",description="This is race 1")
        race2=CharacterRace.objects.create(name="race 2",description="This is race 2")
        class1=CharacterClass.objects.create(name="class 1",description="This is class 1")
        class2=CharacterClass.objects.create(name="class 2",description="This is class 2")
        new_game = Game.objects.create(
            host=self.user,
            game_code='WXYZ',
            name='SinglePlayerTestGame',
            max_players=2,
            winning_level=10,
        )
        new_gamer = Gamer.objects.create(
            game=new_game,
            user=self.user,
            nick=nick,
            level=level,
            gender=gender,
            race_slot_1=race1,
            race_slot_2=race2,
            class_slot_1=class1,
            class_slot_2=class2
        )
        response = self.client.get(reverse('games:game_stats', args=(new_game.id,)))
        #from ipdb import set_trace; set_trace()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.template_name)
        self.assertContains(response, nick)
        self.assertContains(response, level)
        self.assertContains(response, gender)
        self.assertContains(response, race1.name)
        self.assertContains(response, race2.name)
        self.assertContains(response, class1.name)
        self.assertContains(response, class2.name)
