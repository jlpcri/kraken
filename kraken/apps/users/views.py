from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404


def user_is_superuser(user):
    return user.is_superuser


@user_passes_test(user_is_superuser)
def user_management(request):
    if request.method == 'GET':

        sort_types = [
            'username',
            '-username',
            'last_login',
            '-last_login'
        ]
        users = ''
        sort = request.GET.get('sort', '')
        sort = sort if sort else 'username'

        if sort in sort_types:
            if sort == 'username':
                users = User.objects.all().order_by('username')
            elif sort == '-username':
                users = User.objects.all().order_by('-username')
            elif sort == 'last_login':
                users = User.objects.all().order_by('last_login')
            elif sort == '-last_login':
                users = User.objects.all().order_by('-last_login')

        current_user_id = request.user.id

        context = {
            'users': users,
            'sort': sort,
            'current_user_id': current_user_id
        }

        return render(request, 'users/user_management.html', context)

    return HttpResponseNotFound()


@user_passes_test(user_is_superuser)
def user_update(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(User, pk=user_id)

        user.is_active = request.POST.get('is_active', False) \
            or request.POST.get('is_staff', False) \
            or request.POST.get('is_superuser', False)
        user.is_staff = request.POST.get('is_staff', False) \
            or request.POST.get('is_superuser', False)
        user.is_superuser = request.POST.get('is_superuser', False)

        user.save()

        return redirect('users:user_management')
    else:
        return redirect('users:user_management')


@user_passes_test(user_is_superuser)
def user_delete(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if user == request.user:
        logout(request)
        user.delete()
        return redirect('core:landing')
    else:
        user.delete()
        return redirect('users:user_management')
