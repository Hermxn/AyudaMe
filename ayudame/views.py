from django.http import HttpResponse


def start_page(request):
    return HttpResponse("Hello")
