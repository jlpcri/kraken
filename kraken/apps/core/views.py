from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from kraken.apps.core.models import Client, ClientSchema
from kraken.apps.core import messages


@login_required
@csrf_exempt
def create_client(request):
    if request.method == "POST":
        client_name = request.POST.get('client_name')
        print client_name
    return HttpResponseNotFound


@login_required
def home(request):
    return render(request, 'core/home.html')


def landing(request):
    if request.user.is_authenticated():
        return redirect('core:home')
    return render(request, 'core/landing.html')


def sign_in(request):
    if request.method == "POST":
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            if user.is_active:
                login(request, user)

                if request.GET.get('next'):
                    return redirect(request.GET['next'])
                else:
                    return redirect('core:home')
            else:
                messages.danger(request, 'This account is inactive.')
                return redirect('core:landing')
        else:
            messages.danger(request, 'Invalid username or password.')
            return redirect('core:landing')
    else:
        return redirect('core:landing')


@login_required
def sign_out(request):
    logout(request)
    return redirect('core:landing')


def clients_list(request):
    """
    :param request:
    :return: JSON list of client names as string, ordered alphabetically
    """
    clients = Client.objects.all().order_by('name')
    data = {}

    data['client_name'] = [client.name for client in clients]

    return HttpResponse(json.dumps(data), content_type='application/json')


