from django.test import TestCase, Client
from django.core.urlresolvers import reverse, resolve

from kraken.apps.schemas.views import schemas


class TestSchemaViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('schemas:schemas')

    def test_schemas_url_resolve_to_view(self):
        found = resolve(self.url)
        self.assertEqual(found.func, schemas)

    def test_schemas_url_return_status_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)