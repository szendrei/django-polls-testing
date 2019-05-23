from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from polls.views import main_page

class MainPageTest(TestCase):

    def test_root_url_resolves_to_main_page(self):
        main = resolve('/')
        self.assertEqual(main.func, main_page)

    def test_main_page_returns_correct_HTML(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
