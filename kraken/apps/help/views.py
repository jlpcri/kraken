from django.shortcuts import render


def help_guide(request):
    context = {
        'base_url': 'http://' + request.get_host()
    }

    return render(request, 'help/guide.html', context)


def help_faq(request):
    return render(request, 'help/faq.html')