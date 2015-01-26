from django.test import Client, TestCase
from django.core.urlresolvers import reverse, resolve

from kraken.apps.users.views import home


class TestHomeView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('home')

    def test_home_url_resolve_to_view(self):
        found = resolve(self.url)
        self.assertEqual(found.func, home)

    def test_home_url_returns_redirect(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

