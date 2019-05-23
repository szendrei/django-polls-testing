from django.urls import resolve
from django.test import TestCase
from polls.views import main_page

class MainPageTest(TestCase):

    def test_root_url_resolves_to_main_page(self):
        main = resolve('/')
        self.assertEqual(main.func, main_page)
