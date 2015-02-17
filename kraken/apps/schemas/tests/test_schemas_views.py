from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.core.urlresolvers import reverse, resolve

from kraken.apps.core.models import Client as KrakenClient
from kraken.apps.schemas.views import create_schema, create_version, edit_version


class TestSchemaViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.kraken_client = KrakenClient.objects.create(name='Kraken Client')
        self.url_create_schema = reverse(
            'schemas:create_schema',
            args=[self.kraken_client.id, ]
        )
        self.new_schema = {
            'state': 'create',
            'name': 'new schema',
            'identifier': 'new identifier'
        }
        self.user_account = {
            'username': 'Test Username',
            'password': 'Test Password',
        }
        self.user = User.objects.create_user(
            username=self.user_account['username'],
            password=self.user_account['password'],
        )
        self.client.login(
            username=self.user_account['username'],
            password=self.user_account['password']
        )

    def test_create_schemas_url_resolve_to_view(self):
        found = resolve(self.url_create_schema)
        self.assertEqual(found.func, create_schema)

    def test_create_schemas_url_get_return_status_200(self):
        response = self.client.get(self.url_create_schema)
        self.assertEqual(response.status_code, 200)

    def test_create_schemas_url_post_return_status_200(self):
        response = self.client.post(self.url_create_schema, self.new_schema)
        self.assertEqual(response.status_code, 200)