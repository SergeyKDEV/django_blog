from django.shortcuts import render


def page_not_found(request, exception):
    return render(request, '404.html', status=404)


def internal_server_error(request):
    return render(request, '500.html', status=500)


def csrf_failure(request, reason=''):
    return render(request, '403csrf.html', status=403)
