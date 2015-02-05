import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from kraken.apps.core import messages
from kraken.apps.core.models import Client, ClientSchema
from kraken.apps.core.forms import ClientSchemaForm
from kraken.apps.schemas.models import SchemaVersion, VersionBatch, SchemaColumn


@login_required
@csrf_exempt
def create_file(request):
    if request.method == "POST":
        file_name = request.POST.get('file_name')
        print file_name
    return HttpResponseNotFound()


@login_required
def create_schema(request, client_id):
    if request.method == "GET":
        client = get_object_or_404(Client, pk=client_id)
        client_schemas = ClientSchema.objects.filter(client=client)
        context = {
            'client': client,
            'state': 'create',
            'schema_form': ClientSchemaForm(),
            'client_schemas': client_schemas
        }
        return render(request, "schemas/schemas.html", context)
    return HttpResponseNotFound()


@login_required
def edit_schema(request, client_id):
    if request.method == "GET":
        print client_id
        return render(request, "schemas/schemas.html", {'state': 'edit'})
    return HttpResponseNotFound()


@login_required
@csrf_exempt
def create_version(request):
    if request.method == "POST":
        version_name = request.POST.get('version')
        print version_name
    return HttpResponseNotFound()


@login_required
def save_schema(request):
    if request.method == "POST":
        schema_form = ClientSchemaForm(request.POST)
        try:
            if schema_form.is_valid():
                schema = schema_form.save()
                messages.success(request, 'Schema \"{0}\" has been created.'.format(schema.name))
                return redirect('core:home')
            else:
                if schema_form['name'].errors:
                    errors_message = schema_form['name'].errors
                else:
                    errors_message = 'No Client Foreign key provided.'
                messages.danger(request, errors_message)
                return redirect('schemas:create_schema', 1)
        except Exception as e:
            messages.danger(request, e.message)
            return redirect('core:home')
    return HttpResponseNotFound()



def schemas(request):
    return render(request, 'schemas/schemas.html')


def client_schema_new(request):
    pass


def client_schemas_list(request, client_id):
    """
    :param request:
    :param client_name: matching client name
    :return: JSON list of schema names for matching client, ordered alphabetically
    """
    client = get_object_or_404(Client, pk=client_id)
    schemas = ClientSchema.objects.filter(client=client).order_by('name')
    data = {}

    data['client_schema'] = [schema.name for schema in schemas]

    return HttpResponse(json.dumps(data), content_type='application/json')


def schema_version_new(request):
    pass


def schema_version_list(request, schema_id):
    client_schema = get_object_or_404(ClientSchema, pk=schema_id)
    schema_versions = SchemaVersion.objects.filter(client_schema=client_schema)
    data = {}

    data['schema_versions'] = [version.identifier for version in schema_versions]

    return HttpResponse(json.dumps(data), content_type='application/json')


def schema_version_edit(request, schema_id):
    pass



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

    return HttpResponseNotFound()