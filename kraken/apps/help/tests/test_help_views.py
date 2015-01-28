from django.test import TestCase, Client
from django.core.urlresolvers import reverse, resolve

from kraken.apps.help.views import help_guide, help_faq


class TestHelpViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.url_guide = reverse('help:help_guide')
        self.url_faq = reverse('help:help_faq')

    def test_guide_url_resolve_to_view(self):
        found = resolve(self.url_guide)
        self.assertEqual(found.func, help_guide)

    def test_guide_url_return_status_200(self):
        response = self.client.get(self.url_guide)
        self.assertEqual(response.status_code, 200)

    def test_faq_url_resolve_to_view(self):
        found = resolve(self.url_faq)
        self.assertEqual(found.func, help_faq)

    def test_fqa_url_return_status_200(self):
        response = self.client.get(self.url_faq)
        self.assertEqual(response.status_code, 200)