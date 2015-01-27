import json
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from kraken.apps.core.models import Client, ClientSchema


def landing(request):
    if request.user.is_authenticated():
        return redirect('home')
    return render(request, 'landing.html')


def clients_list(request):
    """
    :param request:
    :return: JSON list of client names as string, ordered alphabetically
    """
    clients = Client.objects.all().order_by('name')
    data = {}

    data['client_name'] = [client.name for client in clients]

    return HttpResponse(json.dumps(data), content_type='application/json')


def client_schemas_list(request, client_name):
    """
    :param request:
    :param client_name: matching client name
    :return: JSON list of schema names for matching client, ordered alphabetically
    """
    client = get_object_or_404(Client, name=client_name)
    schemas = ClientSchema.objects.filter(client=client).order_by('name')
    data = {}

    data['client_schema'] = [schema.name for schema in schemas]

    return HttpResponse(json.dumps(data), content_type='application/json')