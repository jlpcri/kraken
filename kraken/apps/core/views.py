from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from kraken.apps.core import messages


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