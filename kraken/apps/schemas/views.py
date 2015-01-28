import json
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404

from kraken.apps.core.models import Client, ClientSchema
from kraken.apps.schemas.models import SchemaVersion, VersionBatch, SchemaColumn


def schemas(request):
    return render(request, 'schemas/schemas.html')


def schema_versions(request):
    """
    :param request:
    :return: JSON list of schema versions of client_name and schema_name
    """
    if request.method == 'GET':
        client_name = request.GET.get('client_name', '')
        schema_name = request.GET.get('schema_name', '')

        client = get_object_or_404(Client, name=client_name)
        client_schema = get_object_or_404(ClientSchema, name=schema_name, client=client)
        schema_versions = SchemaVersion.objects.filter(client_schema=client_schema)
        data = {}

        data['schema_versions'] = [version.identifier for version in schema_versions]

        return HttpResponse(json.dumps(data), content_type='application/json')

    return HttpResponseNotFound


def batch_files(request):
    """
    :param request:
    :return: JSON-encoded list of saved batch files
    """
    if request.method == 'GET':
        client_name = request.GET.get('client_name', '')
        schema_name = request.GET.get('schema_name', '')
        schema_version_identifier = request.GET.get('schema_version_identifier', '')

        client = get_object_or_404(Client, name=client_name)
        client_schema = get_object_or_404(ClientSchema, name=schema_name, client=client)
        schema_version = get_object_or_404(SchemaVersion,
                                           client_schema=client_schema,
                                           identifier=schema_version_identifier)
        version_batch_files = VersionBatch.objects.filter(schema_version=schema_version)
        data = []

        for item in version_batch_files:
            temp = {}
            temp['name'] = item.identifier
            temp['url'] = item.batch_file_path
            temp['last_opened'] = item.last_opened

            data.append(temp)

        return HttpResponse(json.dumps(data), content_type='application/json')

    return HttpResponseNotFound