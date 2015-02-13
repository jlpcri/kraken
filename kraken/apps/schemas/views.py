import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from kraken.apps.core import messages
from kraken.apps.core.models import Client, ClientSchema, SchemaVersion, VersionBatch, SchemaColumn
from kraken.apps.core.forms import ClientSchemaForm, SchemaVersionForm, VersionFileForm


@login_required
@csrf_exempt
def create_file(request, client_id, schema_id, version_id):
    if request.method == "GET":
        client = get_object_or_404(Client, pk=client_id)
        schema = get_object_or_404(ClientSchema, pk=schema_id)
        version = get_object_or_404(SchemaVersion, pk=version_id)
        context = {
            'client': client,
            'schema': schema,
            'version': version,
            'state': 'create',
            'file_form': VersionFileForm
        }
        return render(request, "schemas/file_editor.html", context)
    return HttpResponseNotFound()


@login_required
def create_schema(request, client_id):
    if request.method == "GET":
        client = get_object_or_404(Client, pk=client_id)
        context = {
            'client': client,
            'state': 'create',
            'schema_form': ClientSchemaForm(),
            'version_form': SchemaVersionForm({'delimiter': SchemaVersion.FIXED})
        }
        return render(request, "schemas/schema_editor.html", context)
    return HttpResponseNotFound()


@login_required
@csrf_exempt
def create_version(request, client_id, schema_id):
    if request.method == "POST":
        version_name = request.POST.get('version')
        print version_name
    return HttpResponseNotFound()


@login_required
def edit_file(request, client_id, schema_id, version_id, file_id):
    if request.method == "GET":
        client = get_object_or_404(Client, pk=client_id)
        schema = get_object_or_404(ClientSchema, pk=schema_id)
        version = get_object_or_404(SchemaVersion, pk=version_id)
        context = {
            'client': client,
            'schema': schema,
            'version': version,
            'state': 'edit',
            'file_form': VersionFileForm
        }
        return render(request, "schemas/file_editor.html", context)
    return HttpResponseNotFound()


@login_required
def download_file(request, client_id, schema_id, version_id, file_id):
    if request.method == "GET":
        client = get_object_or_404(Client, pk=client_id)
        schema = get_object_or_404(ClientSchema, pk=schema_id)
        version = get_object_or_404(SchemaVersion, pk=version_id)
        file = get_object_or_404(SchemaVersion, pk=version_id)
        return render(request, "schemas/home.html")
    return HttpResponseNotFound()

@login_required
def edit_version(request, client_id, schema_id, version_id):
    if request.method == "GET":
        client = get_object_or_404(Client, pk=client_id)
        schema = get_object_or_404(ClientSchema, pk=schema_id)
        version = get_object_or_404(SchemaVersion, pk=version_id)
        client_schemas = ClientSchema.objects.filter(client=client)
        context = {
            'client': client,
            'schema': schema,
            'version': version,
            'state': 'edit',
            'schema_form': ClientSchemaForm(),
            'version_form': SchemaVersionForm({'delimiter': SchemaVersion.FIXED}),
            'client_schemas': client_schemas
        }
        return render(request, "schemas/schema_editor.html", context)
    return HttpResponseNotFound()


@login_required
def save_file(request, client_id, schema_id, version_id):
    if request.method == "POST":
        if 'save_file' in request.POST:
            file_form = VersionFileForm(request.POST)
            try:
                if file_form.is_valid():
                    file = file_form.save(commit=False)
                    file.schema_version = get_object_or_404(SchemaVersion, pk=version_id)
                    file.save()
                    messages.success(request, 'File \"{0}\" has been created'.format(file.name))
                    return redirect('core:home')
                else:
                    if file_form['name'].errors:
                        errors_message = file_form['name'].errors
                    else:
                        errors_message = 'Something went wrong'
                    messages.danger(request, errors_message)
                    return redirect('schemas:create_file', client_id, schema_id, version_id)
            except Exception as e:
                messages.danger(request, e.message)
                return redirect('core:home')

    return HttpResponseNotFound()

@login_required
def save_schema(request, client_id):
    if request.method == "POST":
        schema_form = ClientSchemaForm(request.POST)
        version_form = SchemaVersionForm(request.POST)
        client = get_object_or_404(Client, pk=client_id)
        # for r in request.POST:
        #     print r

        state = request.POST.get('state')
        if state == "create":
            try:
                if schema_form.is_valid() and version_form.is_valid():
                    schema = schema_form.save()
                    version = version_form.save(commit=False)
                    version.client_schema = schema
                    version.save()
                    messages.success(request, 'Schema \"{0}\" and Version \"{1}\" have been created'.format(schema.name, version.identifier))
                    return redirect('core:home')
                else:
                    errors_message = "Something went wrong"
                    if not schema_form.is_valid():
                        if schema_form['name'].errors:
                            errors_message = schema_form['name'].errors
                        else:
                            errors_message = 'Schema Name field is not a valid value'
                    elif not version_form.is_valid():
                        if version_form['identifier'].errors:
                            errors_message = version_form['identifier'].errors
                        else:
                            errors_message = 'Version Name field is not a valid value'
                    messages.danger(request, errors_message)
                    context = {
                        'client': client,
                        'state': 'create',
                        'schema_form': schema_form,
                        'version_form': version_form
                    }
                    return render(request, "schemas/schema_editor.html", context)
            except Exception as e:
                messages.danger(request, e.message)
                context = {
                    'client': client,
                    'state': 'create',
                    'schema_form': schema_form,
                    'version_form': version_form
                }
                return render(request, "schemas/schema_editor.html", context)
        elif state == "edit":
            try:
                pass
            except Exception as e:
                messages.danger(request, e.message)
                context = {
                    'client': client,
                    'state': 'edit',
                    'schema_form': schema_form,
                    'version_form': version_form
                }
                return render(request, "schemas/schema_editor.html", context)
    return HttpResponseNotFound()


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




def schema_version_list(request, schema_id):
    client_schema = get_object_or_404(ClientSchema, pk=schema_id)
    schema_versions = SchemaVersion.objects.filter(client_schema=client_schema)
    data = {}

    data['schema_versions'] = [version.identifier for version in schema_versions]

    return HttpResponse(json.dumps(data), content_type='application/json')



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