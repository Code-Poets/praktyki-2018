from django.test import TestCase
from games.forms import GamerForm
from games.models import Gamer, Gender, CharacterRace, CharacterClass


class GamerFormTests(TestCase):

    def setUp(self):
        self.gamer = Gamer(
            nick='MrNobody'
        )

        self.charrace = CharacterRace.objects.create(
            name='Race',
            description='This is a race'
        )

        self.charclass = CharacterClass.objects.create(
            name='Class',
            description='This is a class'
        )

    def test_required_fields_valid(self):
        form=GamerForm(data={
            'level': 1,
            'bonus': 0,
            'gender': Gender.N.value,
        }, instance=self.gamer)
        self.assertTrue(form.is_valid())

    def test_status_field_valid(self):
        form=GamerForm(data={
            'status': "I'm OK",
            'level': 1,
            'bonus': 0,
            'gender': Gender.N.value,
        }, instance=self.gamer)
        self.assertTrue(form.is_valid())

    def test_race_slot_1_valid(self):
        form=GamerForm(data={
            'level': 1,
            'bonus': 0,
            'gender': Gender.N.value,
            'race_slot_1': self.charrace.id
        }, instance=self.gamer)
        self.assertTrue(form.is_valid())

    def test_race_slot_2_valid(self):
        form=GamerForm(data={
            'level': 1,
            'bonus': 0,
            'gender': Gender.N.value,
            'race_slot_2': self.charrace.id
        }, instance=self.gamer)
        self.assertTrue(form.is_valid())

    def test_class_slot_1_valid(self):
        form=GamerForm(data={
            'level': 1,
            'bonus': 0,
            'gender': Gender.N.value,
            'class_slot_1': self.charclass.id
        }, instance=self.gamer)
        self.assertTrue(form.is_valid())

    def test_class_slot_2_valid(self):
        form=GamerForm(data={
            'level': 1,
            'bonus': 0,
            'gender': Gender.N.value,
            'class_slot_2': self.charclass.id
        }, instance=self.gamer)
        self.assertTrue(form.is_valid())

    def test_level_field_blank(self):
        form=GamerForm(data={
            'level': None,
            'bonus': 0,
            'gender': Gender.N.value,
        }, instance=self.gamer)
        self.assertFalse(form.is_valid())

    def test_bonus_field_blank(self):
        form=GamerForm(data={
            'level': 1,
            'bonus': None,
            'gender': Gender.N.value,
        }, instance=self.gamer)
        self.assertFalse(form.is_valid())

    def test_gender_field_blank(self):
        form=GamerForm(data={
            'level': 1,
            'bonus': 0,
            'gender': None,
        }, instance=self.gamer)
        self.assertFalse(form.is_valid())

    def test_level_field_invalid(self):
        form=GamerForm(data={
            'level': 0,
            'bonus': 0,
            'gender': Gender.N.value,
        }, instance=self.gamer)
        self.assertFalse(form.is_valid())
