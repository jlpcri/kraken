from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from kraken.apps.core.models import Client, ClientSchema
from kraken.apps.core import messages
from kraken.apps.core.forms import ClientForm


@login_required
def home(request):
    clients = Client.objects.all().order_by('name')
    context = {
        'clients': clients,
        'form': ClientForm()
    }
    return render(request, 'core/home.html', context)


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


@login_required
@csrf_exempt
def create_client(request):
    """
    Handle create new client with valid client name
    :param request:
    :return: if succeed, back to home
             if un-succeed, back to create client modal with error message
    """
    if request.method == "POST":
        form = ClientForm(request.POST)
        try:
            if form.is_valid():
                client = form.save()
                messages.success(request, 'Client \"{0}\" has been created.'.format(client.name))
                return HttpResponse(json.dumps({'success': True}))
            else:
                context = {
                    'success': False,
                }
                if form['name'].errors:
                    context['error'] = form['name'].errors
        except Exception as e:
            context = {
                'success': False,
                'error': e.message
            }

        return HttpResponse(json.dumps(context))
    else:
        redirect('core:home')



