from django.core.urlresolvers import resolve
from django.test import TestCase
from lists.views import home_page

class HomeTestCase(TestCase):

    def test_root_url_resolves_to_home_page_url(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
