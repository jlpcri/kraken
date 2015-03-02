from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.core.urlresolvers import reverse, resolve

from kraken.apps.core.models import Client as KrakenClient, ClientSchema, SchemaVersion
from kraken.apps.schemas.views import create_file


class TestVersionFiles(TestCase):
    def setUp(self):
        self.client = Client()
        self.kraken_client = KrakenClient.objects.create(name='Kraken Client')
        self.kraken_schema = ClientSchema.objects.create(name='Client Schema', client=self.kraken_client)
        self.kraken_version = SchemaVersion.objects.create(identifier='New Identifier', client_schema=self.kraken_schema)

        self.url_create_file = reverse(
            'schemas:create_file',
            args=[self.kraken_client.id, self.kraken_schema.id, self.kraken_version.id]
        )
        self.new_file_valid = {
            'name': 'File A',
            'save_file': '',
            'textareaViewer': 'aaaaabbbbb'
        }
        self.new_file_empty_contents = {
            'name': 'File A',
            'save_file': '',
            'textareaViewer': ''
        }
        self.new_file_empty_filename = {
            'name': '',
            'save_file': '',
            'textareaViewer': 'aaaaabbbbb'
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

    def test_create_files_url_resolve_to_view(self):
        found = resolve(self.url_create_file)
        self.assertEqual(found.func, create_file)

    def test_create_files_url_get_return_status_200(self):
        response = self.client.get(self.url_create_file)
        self.assertEqual(response.status_code, 200)

    def test_create_files_url_post_with_valid_data_return_status_200(self):
        response = self.client.post(self.url_create_file, self.new_file_valid, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_create_files_url_post_with_empty_contents_receive_error(self):
        response = self.client.post(self.url_create_file, self.new_file_empty_contents, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No input of contents')

    def test_create_files_url_post_with_empty_filename_receive_error(self):
        response = self.client.post(self.url_create_file, self.new_file_empty_filename, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'File Name field is required')




