import json
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.files.base import ContentFile
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from kraken.apps.core import messages
from kraken.apps.core.models import Client, ClientSchema, SchemaVersion, VersionFile, FileColumn, SchemaColumn
from kraken.apps.core.forms import ClientSchemaForm, SchemaVersionForm, VersionFileForm


def user_is_staff(user):
    return user.is_staff


@login_required
@csrf_exempt
def create_file(request, client_id, schema_id, version_id):
    """
    Fetch needed information for create file
    :param request:
    :param client_id: id of client
    :param schema_id: id of schema
    :param version_id: id of version
    :return: needed infomation for preparing create new file
    """
    if request.method == "GET":
        client = get_object_or_404(Client, pk=client_id)
        schema = get_object_or_404(ClientSchema, pk=schema_id)
        version = get_object_or_404(SchemaVersion, pk=version_id)
        version_files_names = []
        for item in version.files():
            version_files_names.append(item.name)

        fields = SchemaColumn.objects.filter(schema_version=version).order_by('position')

        context = {
            'client': client,
            'schema': schema,
            'version': version,
            'fields': fields,
            'field_number': len(fields),
            'field_types': [item[1] for item in FileColumn.GENERATOR_CHOICES],
            'state': 'create',
            'file_form': VersionFileForm,
            'version_files_names': json.dumps(version_files_names)
        }
        return render(request, "schemas/file_editor.html", context)
    if request.method == "POST":
        if 'save_file' in request.POST:
            client = get_object_or_404(Client, pk=client_id)
            schema = get_object_or_404(ClientSchema, pk=schema_id)
            version = get_object_or_404(SchemaVersion, pk=version_id)
            fields = SchemaColumn.objects.filter(schema_version=version).order_by('position')
            file_form = VersionFileForm(request.POST)
            payloads = request.POST.get('payloads')

            try:
                if file_form.is_valid():
                    file = file_form.save(commit=False)
                    file.schema_version = get_object_or_404(SchemaVersion, pk=version_id)
                    file.contents.save(file.name, ContentFile(request.POST.get('textareaViewer', '')))
                    file.save()
                    messages.success(request, 'File \"{0}\" has been created'.format(file.name))
                    return redirect('core:home')
                else:
                    if file_form['name'].errors:
                        error_message = file_form['name'].errors
                    else:
                        error_message = 'Something went wrong'
                    messages.danger(request, error_message)
                    context = {
                        'client': client,
                        'schema': schema,
                        'version': version,
                        'fields': fields,
                        'field_number': len(fields),
                        'field_types': [item[1] for item in FileColumn.GENERATOR_CHOICES],
                        'state': 'create',
                        'file_form': VersionFileForm,
                        'payloads': payloads
                    }
                    return render(request, "schemas/file_editor.html", context)
            except Exception as e:
                messages.danger(request, e.message)
                context = {
                    'client': client,
                    'schema': schema,
                    'version': version,
                    'fields': fields,
                    'field_number': len(fields),
                    'field_types': [item[1] for item in FileColumn.GENERATOR_CHOICES],
                    'state': 'create',
                    'file_form': VersionFileForm,
                    'payloads': payloads
                }
                return render(request, "schemas/file_editor.html", context)
    return HttpResponseNotFound()


@login_required
@user_passes_test(user_is_staff)
def create_schema(request, client_id):
    """
    Handles GET requests to display schema editor for inputting new schema
            returns 200 or 404
            POST requests to save new schema to database
            returns 200 or 404
    """
    if request.method == "GET":
        client = get_object_or_404(Client, pk=client_id)
        context = {
            'client': client,
            'state': 'create',
            'schema_form': ClientSchemaForm(),
            'version_form': SchemaVersionForm({'delimiter': SchemaVersion.FIXED})
        }
        return render(request, "schemas/schema_editor.html", context)
    elif request.method == "POST":
        client = get_object_or_404(Client, pk=client_id)
        schema, schema_created = ClientSchema.objects.get_or_create(client=client, name=request.POST.get('name'))
        version, version_created = SchemaVersion.objects.get_or_create(client_schema=schema, identifier=request.POST.get('identifier'))
        schema_form = ClientSchemaForm(request.POST, instance=schema)
        version_form = SchemaVersionForm(request.POST, instance=version)
        columns = version.validate_columns(request.POST)

        try:
            if schema_form.is_valid() and version_form.is_valid() and columns.get('valid') is not False:
                schema = schema_form.save()
                version = version_form.save(commit=False)
                version.client_schema = schema
                version.save()
                columns = version.save_columns(columns)
                messages.success(request, 'Schema \"{0}\" and Version \"{1}\" have been updated'.format(schema.name, version.identifier))
                return redirect('schemas:edit_version', client_id, schema.pk, version.pk)
            else:
                error_message = "Something went wrong"
                if not schema_form.is_valid():
                    if schema_form['name'].errors:
                        error_message = schema_form['name'].errors
                    elif schema_form.errors:
                        error_message = schema_form.errors
                    else:
                        error_message = 'Schema Name is not a valid value'
                elif not version_form.is_valid():
                    if version_form['identifier'].errors:
                        error_message = version_form['identifier'].errors
                    elif version_form.errors:
                        error_message = version_form.errors
                    else:
                        error_message = 'Version Name is not a valid value'
                elif columns.get('valid') is False:
                    error_message = columns.get('error_message')
                messages.danger(request, error_message)
                context = {
                    'client': client,
                    'state': 'create',
                    'schema_form': schema_form,
                    'version_form': version_form,
                    'fields': columns.get('fields')
                }
                return render(request, "schemas/schema_editor.html", context)
        except Exception as e:
            version.delete()
            schema.delete()
            messages.danger(request, e.message)
            context = {
                'client': client,
                'state': 'create',
                'schema_form': schema_form,
                'version_form': version_form,
                'fields': columns.get('fields')
            }
            return render(request, "schemas/schema_editor.html", context)
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
    """
    Handles GET requests to download file to client computer
            returns 200 or 404
    """
    if request.method == "GET":
        client = get_object_or_404(Client, pk=client_id)
        schema = get_object_or_404(ClientSchema, pk=schema_id)
        version = get_object_or_404(SchemaVersion, pk=version_id)
        f = get_object_or_404(VersionFile, pk=file_id)
        response = HttpResponse(f.contents, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="{0}.txt"'.format(f.name)
        #response.write(f.contents)
        return response
    return HttpResponseNotFound()


@login_required
@user_passes_test(user_is_staff)
def edit_version(request, client_id, schema_id, version_id):
    """
    Handles GET requests to display an already created schema version for editing
            returns 200 or 404
            POST requests to save edited schema to database
            returns 200 or 404
    """
    if request.method == "GET":
        client = get_object_or_404(Client, pk=client_id)
        schema = get_object_or_404(ClientSchema, pk=schema_id)
        version = get_object_or_404(SchemaVersion, pk=version_id)
        context = {
            'client': client,
            'schema': schema,
            'version': version,
            'state': 'edit',
            'schema_form': ClientSchemaForm(instance=schema),
            'version_form': SchemaVersionForm(instance=version),
            'fields': version.get_columns(position_order=True)
        }
        return render(request, "schemas/schema_editor.html", context)
    elif request.method == "POST":
        client = get_object_or_404(Client, pk=client_id)
        schema = get_object_or_404(ClientSchema, pk=schema_id)
        version = get_object_or_404(SchemaVersion, pk=version_id)
        schema_form = ClientSchemaForm(request.POST, instance=schema)
        version_form = SchemaVersionForm(request.POST, instance=version)
        columns = version.validate_columns(request.POST)

        if 'save_schema' in request.POST:
            try:
                if schema_form.is_valid() and version_form.is_valid() and columns.get('valid') is not False:
                    schema = schema_form.save()
                    version = version_form.save(commit=False)
                    version.client_schema = schema
                    version.save()
                    columns = version.save_columns(columns)
                    messages.success(request, 'Schema \"{0}\" and Version \"{1}\" have been updated'.format(schema.name, version.identifier))
                    return redirect('schemas:edit_version', client_id, schema_id, version_id)
                else:
                    error_message = "Something went wrong"
                    if not schema_form.is_valid():
                        if schema_form['name'].errors:
                            error_message = schema_form['name'].errors
                        elif schema_form.errors:
                            error_message = schema_form.errors
                        else:
                            error_message = 'Schema Name is not a valid value'
                    elif not version_form.is_valid():
                        if version_form['identifier'].errors:
                            error_message = version_form['identifier'].errors
                        elif version_form.errors:
                            error_message = version_form.errors
                        else:
                            error_message = 'Version Name is not a valid value'
                    elif columns.get('valid') is False:
                        error_message = columns.get('error_message')
                    messages.danger(request, error_message)
                    context = {
                        'client': client,
                        'schema': schema,
                        'version': version,
                        'state': 'edit',
                        'schema_form': schema_form,
                        'version_form': version_form,
                        'fields': columns.get('fields')
                    }
                    return render(request, "schemas/schema_editor.html", context)
            except Exception as e:
                messages.danger(request, e.message)
                context = {
                    'client': client,
                    'schema': schema,
                    'version': version,
                    'state': 'edit',
                    'schema_form': schema_form,
                    'version_form': version_form,
                    'fields': columns.get('fields')
                }
                return render(request, "schemas/schema_editor.html", context)
        elif 'save_version' in request.POST:
            version.identifier = request.POST.get('modal_version_name')
            try:
                version.save()
                messages.success(request, 'Version \"{0}\" has been updated'.format(version.identifier))
                return redirect('schemas:edit_version', client_id, schema_id, version_id)
            except Exception as e:
                messages.danger(request, e.message)
                return redirect('schemas:edit_version', client_id, schema_id, version_id)

        elif 'create_version' in request.POST:
            try:
                version_new = SchemaVersion.objects.create(identifier=request.POST.get('modal_version_name'),
                                                           client_schema=version.client_schema,
                                                           delimiter=version.delimiter)
                cols = version.get_columns(position_order=True)
                for col in cols:
                    SchemaColumn.objects.create(
                        position=col.position,
                        schema_version=version_new,
                        name=col.name,
                        type=col.type,
                        length=col.length
                    )

                messages.success(request, 'Version \"{0}\" has been created'.format(version_new.identifier))
                return redirect('schemas:edit_version', client_id, schema_id, version_new.id)
            except Exception as e:
                messages.danger(request, e.message)
                return redirect('schemas:edit_version', client_id, schema_id, version_id)

    return HttpResponseNotFound()


def clients_list(request):
    """
    Handle fetch client list as json
    :param request:
    :return: json list of client names
    """
    clients = Client.objects.all().order_by('name')

    data = {}
    data['clients'] = [client.name for client in clients]

    return HttpResponse(json.dumps(data), content_type='application/json')


def client_schemas_list(request, client_name):
    """
    :param request:
    :param client_name: matching client name
    :return: JSON list of schema names for matching client, ordered alphabetically
    """
    data = {}
    try:
        client = get_object_or_404(Client, name=client_name)
        schemas = client.schemas()
        data['client_schemas'] = [schema.name for schema in schemas]
    except Exception as e:
        data['error'] = e.message

    return HttpResponse(json.dumps(data), content_type='application/json')


def schema_versions_list(request, client_name, schema_name):
    """
    Return json list of client-schema-versions
    :param request:
    :param client_name: matching client name
    :param schema_name: matching schema name
    :return: json list of versions identifier
    """
    data = {}
    try:
        client = get_object_or_404(Client, name=client_name)
        client_schema = get_object_or_404(ClientSchema, client=client, name=schema_name)
        schema_versions = client_schema.versions()

        data['schema_versions'] = [version.identifier for version in schema_versions]
    except Exception as e:
        data['error'] = e.message

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
        version_files = VersionFile.objects.filter(schema_version=schema_version)
        data = []

        for item in version_files:
            temp = {}
            temp['name'] = item.name
            temp['url'] = item.batch_file_path
            temp['last_opened'] = item.last_opened

            data.append(temp)

        return HttpResponse(json.dumps(data), content_type='application/json')

    return HttpResponseNotFound()