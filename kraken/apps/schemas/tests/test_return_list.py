from django.test import TestCase, Client
import json

from kraken.apps.core.models import Client as KrakenClient, ClientSchema, SchemaVersion
from kraken.apps.schemas.views import client_schemas_list, schema_versions_list


class TestReturnList(TestCase):
    def setUp(self):
        self.client = Client()
        self.client1 = KrakenClient.objects.create(name='First Client')
        self.client2 = KrakenClient.objects.create(name='Second Client')
        self.client3 = KrakenClient.objects.create(name='Third Client')
        self.client4 = KrakenClient.objects.create(name='Fourth Client')

        self.client1_schema1 = ClientSchema.objects.create(
            client=self.client1,
            name='Client1 Schema1'
        )
        self.client1_schema2 = ClientSchema.objects.create(
            client=self.client1,
            name='Client1 Schema2'
        )
        self.client1_schema3 = ClientSchema.objects.create(
            client=self.client1,
            name='Client1 Schema3'
        )
        self.client1_schema4 = ClientSchema.objects.create(
            client=self.client1,
            name='Client1 Schema4'
        )

        self.client1_schema1_version1 = SchemaVersion.objects.create(
            client_schema=self.client1_schema1,
            identifier='Client1 Schema1 Version1'
        )
        self.client1_schema1_version2 = SchemaVersion.objects.create(
            client_schema=self.client1_schema1,
            identifier='Client1 Schema1 Version2'
        )
        self.client1_schema1_version3 = SchemaVersion.objects.create(
            client_schema=self.client1_schema1,
            identifier='Client1 Schema1 Version3'
        )
        self.client1_schema1_version4 = SchemaVersion.objects.create(
            client_schema=self.client1_schema1,
            identifier='Client1 Schema1 Version4'
        )

    def test_return_lists_of_schemas_of_client(self):
        response = client_schemas_list(None, self.client1.name)
        content = json.loads(response.content)

        self.assertEqual(content.keys()[0], 'client_schemas')
        self.assertContains(response, self.client1_schema1.name)
        self.assertContains(response, self.client1_schema2.name)
        self.assertContains(response, self.client1_schema3.name)
        self.assertContains(response, self.client1_schema4.name)

    def test_return_lists_of_schemas_of_client_with_invalid_input(self):
        response = client_schemas_list(None, 'Wrong Client Name')
        content = json.loads(response.content)

        self.assertEqual(content.keys()[0], 'error')
        self.assertContains(response, 'No Client matches the given query.')

    def test_return_lists_of_versions_of_schemas(self):
        response = schema_versions_list(None, self.client1.name, self.client1_schema1.name)
        content = json.loads(response.content)

        self.assertEqual(content.keys()[0], 'schema_versions')
        self.assertContains(response, self.client1_schema1_version1.identifier)
        self.assertContains(response, self.client1_schema1_version2.identifier)
        self.assertContains(response, self.client1_schema1_version3.identifier)
        self.assertContains(response, self.client1_schema1_version4.identifier)

    def test_return_lists_of_versions_of_schemas_with_invalid_client_name(self):
        response = schema_versions_list(None, 'Wrong Client Name', self.client1_schema1.name)
        content = json.loads(response.content)

        self.assertEqual(content.keys()[0], 'error')
        self.assertContains(response, 'No Client matches the given query.')

    def test_return_lists_of_versions_of_schemas_with_invalid_schema_name(self):
        response = schema_versions_list(None, self.client1.name, 'Wrong Schema Name')
        content = json.loads(response.content)

        self.assertEqual(content.keys()[0], 'error')
        self.assertContains(response, 'No ClientSchema matches the given query.')