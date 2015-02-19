import json
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.core.urlresolvers import reverse, resolve

from kraken.apps.core.views import landing, home, create_client
from kraken.apps.core.models import Client as KrakenClient


class TestCoreView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url_landing = reverse('core:landing')
        self.url_home = reverse('core:home')

    def test_landing_url_resolve_to_view(self):
        found = resolve(self.url_landing)
        self.assertEqual(found.func, landing)

    def test_landing_url_returns_status_200(self):
        response = self.client.get(self.url_landing)
        self.assertEqual(response.status_code, 200)

    def test_home_url_resolve_to_view(self):
        found = resolve(self.url_home)
        self.assertEqual(found.func, home)

    def test_home_url_returns_status_200(self):
        response = self.client.get(self.url_home, follow=True)
        self.assertEqual(response.status_code, 200)


class CreateClientTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('core:create_client')
        self.create_client_valid = {
            'name': 'New Client'
        }
        self.create_client_invalid_without_name = {
            'name': ''
        }
        self.create_client_invalid_with_duplicate_name = {
            'name': 'New Client'
        }
        self.user_account = {
            'username': 'Test Username',
            'password': 'Test Password',
        }
        self.user = User.objects.create_user(
            username=self.user_account['username'],
            password=self.user_account['password'],
        )
        self.staff = User.objects.create_user(
            username='staff_user',
            password='staff_password'
        )
        self.staff.is_staff = True
        self.staff.save()
        self.client.login(
            username=self.user_account['username'],
            password=self.user_account['password']
        )

    def test_client_create_url_resolves_to_view(self):
        found = resolve(self.url)
        self.assertEqual(found.func, create_client)

    def test_client_create_url_return_status_200(self):
        response = self.client.post(self.url, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_whatever_you_call_it(self):
        self.client.logout()
        self.client.login(
            username='staff_user',
            password='staff_password'
        )


    def test_client_create_with_valid_data_successful(self):
        response = self.client.post(self.url, self.create_client_valid)
        client = KrakenClient.objects.get(name=self.create_client_valid['name'])
        self.assertIsNotNone(client)

    def test_client_create_with_valid_data_return_success_json(self):
        response = self.client.post(self.url, self.create_client_valid)
        self.assertContains(response, json.dumps({'success': True}))
