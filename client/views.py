from django.db import transaction
from django.urls import reverse_lazy
from django.views import generic
from django_registration.backends.one_step.views import RegistrationView, login

from .forms import CustomRegistrationForm
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


class CustomRegistrationView(RegistrationView):
    form_class = CustomRegistrationForm
    success_url = reverse_lazy("orders:index")

    @transaction.atomic()
    def form_valid(self, form):
        user = form.save()
        client = Client(
            user=user,
            phone=form.cleaned_data["phone"],
        )
        client.save()
        login(self.request, user)
        return super().form_valid(form)
