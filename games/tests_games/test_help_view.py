from django.test import TestCase
from django.urls import reverse


class HelpViewTests(TestCase):
    def test_help_view(self):
        url = reverse('games:help')
        response = self.client.get(url)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'games/instruction_manual.html')
