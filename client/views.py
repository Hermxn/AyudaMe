from django.views import generic

from .models import Client


class IndexView(generic.ListView):
    template_name = "client/index.html"
    context_object_name = "clients"
    ordering = ["-rating"]
    queryset = Client.objects.all()


class DetailView(generic.DetailView):
    model = Client
    template_name = "client/detail.html"
    context_object_name = "client"
