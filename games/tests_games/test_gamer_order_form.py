from django.test import TestCase
from games.forms.form_gamer_order import GamerOrderForm
from games.models.model_gamer import Gamer
from games.models.enum_gender import Gender
from games.models.model_character_race import CharacterRace
from games.models.model_character_class import CharacterClass
from games.models.model_game import Game
from users.models import CustomUser

class GamerOrderFormTests(TestCase):
    def setUp(self):
        self.charrace = CharacterRace.objects.create(
            name='Race',
            description='This is a race'
        )

        self.charclass = CharacterClass.objects.create(
            name='Class',
            description='This is a class'
        )

        user = CustomUser.objects.create_user(
            username='nobodyuser2',
            email='email2',
            nick='SammyClassicSonicFan'
        )
        user.set_password('nobodypassword')
        user.save()

        game = Game.objects.create(
            host=user,
            game_code='XXXX',
            name='TestGame',
            max_players=2,
            winning_level=10
        )

        gamer = Gamer.objects.create(
            nick='SammyClassicSonicFan',
            game=game,
            order=2
        )

        self.gamer = Gamer.objects.create(
            nick='MrNobody',
            game=game
        )


    def test_required_fields_valid(self):
        form=GamerOrderForm(data={
            'level': 1,
            'bonus': 0,
            'gender': Gender.N.value,
        }, instance=self.gamer)
        self.assertTrue(form.is_valid())

    def test_status_field_valid(self):
        form=GamerOrderForm(data={
            'status': "I'm OK",
            'level': 1,
            'bonus': 0,
            'gender': Gender.N.value,
        }, instance=self.gamer)
        self.assertTrue(form.is_valid())

    def test_race_slot_1_valid(self):
        form=GamerOrderForm(data={
            'level': 1,
            'bonus': 0,
            'gender': Gender.N.value,
            'race_slot_1': self.charrace.id
        }, instance=self.gamer)
        self.assertTrue(form.is_valid())

    def test_race_slot_2_valid(self):
        form=GamerOrderForm(data={
            'level': 1,
            'bonus': 0,
            'gender': Gender.N.value,
            'race_slot_2': self.charrace.id
        }, instance=self.gamer)
        self.assertTrue(form.is_valid())

    def test_class_slot_1_valid(self):
        form=GamerOrderForm(data={
            'level': 1,
            'bonus': 0,
            'gender': Gender.N.value,
            'class_slot_1': self.charclass.id
        }, instance=self.gamer)
        self.assertTrue(form.is_valid())

    def test_class_slot_2_valid(self):
        form=GamerOrderForm(data={
            'level': 1,
            'bonus': 0,
            'gender': Gender.N.value,
            'class_slot_2': self.charclass.id
        }, instance=self.gamer)
        self.assertTrue(form.is_valid())

    def test_level_field_blank(self):
        form=GamerOrderForm(data={
            'level': None,
            'bonus': 0,
            'gender': Gender.N.value,
        }, instance=self.gamer)
        self.assertFalse(form.is_valid())

    def test_bonus_field_blank(self):
        form=GamerOrderForm(data={
            'level': 1,
            'bonus': None,
            'gender': Gender.N.value,
        }, instance=self.gamer)
        self.assertFalse(form.is_valid())

    def test_gender_field_blank(self):
        form=GamerOrderForm(data={
            'level': 1,
            'bonus': 0,
            'gender': None,
        }, instance=self.gamer)
        self.assertFalse(form.is_valid())

    def test_level_field_invalid(self):
        form=GamerOrderForm(data={
            'level': 0,
            'bonus': 0,
            'gender': Gender.N.value,
        }, instance=self.gamer)
        self.assertFalse(form.is_valid())

    def test_valid_order(self):
        form=GamerOrderForm(data={
            'level': 1,
            'bonus': 0,
            'gender': Gender.N.value,
            'order': 1
        }, instance=self.gamer)
        self.assertTrue(form.is_valid())

    def test_invalid_order(self):
        form=GamerOrderForm(data={
            'level': 1,
            'bonus': 0,
            'gender': Gender.N.value,
            'order': -1
        }, instance=self.gamer)
        self.assertFalse(form.is_valid())

    def test_taken_order(self):
        form=GamerOrderForm(data={
            'level': 1,
            'bonus': 0,
            'gender': Gender.N.value,
            'order': 2
        }, instance=self.gamer)

        self.assertFalse(form.is_valid())
