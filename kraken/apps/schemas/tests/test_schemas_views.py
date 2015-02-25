from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.core.urlresolvers import reverse, resolve

from kraken.apps.core.models import Client as KrakenClient, ClientSchema, SchemaVersion
from kraken.apps.schemas.views import create_schema, create_version, edit_version


class TestSchemaViewsAsUser(TestCase):
    def setUp(self):
        self.client = Client()
        self.kraken_client = KrakenClient.objects.create(name='Kraken Client')
        self.kraken_schema = ClientSchema.objects.create(name='Client Schema', client=self.kraken_client)
        self.kraken_version = SchemaVersion.objects.create(identifier='New Identifier', client_schema=self.kraken_schema)

        self.url_create_schema = reverse(
            'schemas:create_schema',
            args=[self.kraken_client.id, ]
        )
        self.url_edit_version = reverse(
            'schemas:edit_version',
            args=[self.kraken_client.id, self.kraken_schema.id, self.kraken_version.id, ]
        )
        self.new_schema = {
            'state': 'create',
            'name': 'new schema',
            'identifier': 'new identifier'
        }
        self.edit_version = {
            'state': 'edit',
            'name': 'edit version',
            'identifier': 'identifier'
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

    def test_create_schemas_url_resolve_to_view_as_user(self):
        found = resolve(self.url_create_schema)
        self.assertEqual(found.func, create_schema)

    def test_create_schemas_url_get_return_status_302_as_user(self):
        response = self.client.get(self.url_create_schema)
        self.assertEqual(response.status_code, 302)

    def test_create_schemas_url_post_return_status_302_as_user(self):
        response = self.client.post(self.url_create_schema, self.new_schema)
        self.assertEqual(response.status_code, 302)

    def test_edit_version_url_resolve_to_view_as_user(self):
        found = resolve(self.url_edit_version)
        self.assertEqual(found.func, edit_version)

    def test_edit_version_url_get_return_status_302_as_user(self):
        response = self.client.get(self.url_edit_version)
        self.assertEqual(response.status_code, 302)

    def test_edit_version_url_post_return_status_302_as_user(self):
        response = self.client.post(self.url_edit_version, self.edit_version)
        self.assertEqual(response.status_code, 302)


class TestSchemaViewsAsStaff(TestCase):
    def setUp(self):
        self.client = Client()
        self.kraken_client = KrakenClient.objects.create(name='Kraken Client')
        self.kraken_schema = ClientSchema.objects.create(name='Client Schema', client=self.kraken_client)
        self.kraken_version = SchemaVersion.objects.create(identifier='New Identifier',
                                                           client_schema=self.kraken_schema)

        self.url_create_schema = reverse(
            'schemas:create_schema',
            args=[self.kraken_client.id, ]
        )
        self.url_edit_version = reverse(
            'schemas:edit_version',
            args=[self.kraken_client.id, self.kraken_schema.id, self.kraken_version.id, ]
        )
        self.new_schema = {
            'state': 'create',
            'name': 'new schema',
            'identifier': 'new identifier'
        }
        self.edit_version = {
            'state': 'edit',
            'save_schema': '',
            'name': self.kraken_schema.name,
            'identifier': self.kraken_version.identifier
        }
        self.edit_version_schema_name_change = {
            'hiddenFieldId_1': self.kraken_client.id,
            'name': 'New Schema Name',
            'delimiter': self.kraken_version.delimiter,
            'inputFieldName_1': 'String5',
            'inputFieldLength_1': 5,
            'selectFieldType_1': 'Text',
            'save_schema': '',
            'state': 'edit',
            'client': self.kraken_client.id,
            'client_id': self.kraken_client.id,
            'row_order': '1 ',
            'identifier': self.kraken_version.identifier
        }
        self.edit_version_version_name_change = {
            'hiddenFieldId_1': self.kraken_client.id,
            'name': self.kraken_schema.name,
            'delimiter': self.kraken_version.delimiter,
            'inputFieldName_1': 'String5',
            'inputFieldLength_1': 5,
            'selectFieldType_1': 'Text',
            'save_schema': '',
            'state': 'edit',
            'client': self.kraken_client.id,
            'client_id': self.kraken_client.id,
            'row_order': '1 ',
            'identifier': self.kraken_version.identifier
        }
        self.user_account = {
            'username': 'Test Username',
            'password': 'Test Password',
        }
        self.staff = User.objects.create_user(
            username=self.user_account['username'],
            password=self.user_account['password'],
        )

        self.staff.is_staff = True
        self.staff.save()

        self.client.login(
            username=self.user_account['username'],
            password=self.user_account['password']
        )

    def test_create_schemas_url_resolve_to_view_as_staff(self):
        found = resolve(self.url_create_schema)
        self.assertEqual(found.func, create_schema)

    def test_create_schemas_url_get_return_status_200_as_staff(self):
        response = self.client.get(self.url_create_schema)
        self.assertEqual(response.status_code, 200)

    def test_create_schemas_url_post_return_status_200_as_staff(self):
        response = self.client.post(self.url_create_schema, self.new_schema)
        self.assertEqual(response.status_code, 200)

    def test_edit_version_url_resolve_to_view_as_staff(self):
        found = resolve(self.url_edit_version)
        self.assertEqual(found.func, edit_version)

    def test_edit_version_url_get_return_status_200_as_staff(self):
        response = self.client.get(self.url_edit_version)
        self.assertEqual(response.status_code, 200)

    def test_edit_version_url_post_return_status_200_as_staff(self):
        response = self.client.post(self.url_edit_version, self.edit_version)
        self.assertEqual(response.status_code, 200)

    def test_edit_version_with_schema_name_update(self):
        response = self.client.post(self.url_edit_version, self.edit_version_schema_name_change)
        self.assertContains(response, self.edit_version_schema_name_change['name'])

    def test_edit_version_with_version_name_update(self):
        response = self.client.post(self.url_edit_version, self.edit_version_version_name_change)
        self.assertContains(response, self.edit_version_version_name_change['identifier'])