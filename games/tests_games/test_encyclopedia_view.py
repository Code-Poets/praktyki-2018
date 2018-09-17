from django.test import TestCase
from django.urls import reverse
from games.models import CharacterRace, CharacterClass
from ipdb import set_trace


class EncyclopediaViewTests(TestCase):
    def setUp(self):
        self.racename = 'Race'
        self.classname = 'Class'
        char_race = CharacterRace.objects.create(
            name=self.racename,
            description='This is a race'
        )

        char_class = CharacterClass.objects.create(
            name=self.classname,
            description='This is a class'
        )

    def test_help_view(self):
        url = reverse('games:encyclopedia')
        response = self.client.get(url)
        #set_trace()
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/encyclopedia.html')
        self.assertContains(response, self.racename)
        self.assertContains(response, self.classname)
