from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from variables import choices

from .forms import OrderCreateForm, OrderUpdateForm
from .models import Client, Order


class OrderIndexView(generic.ListView):
    template_name = "order/index.html"
    ordering = ["-date"]
    queryset = Order.objects.all()
    context_object_name = "orders"

    @staticmethod
    def post(request: HttpRequest) -> HttpResponse:
        filters = list(choices.AREA_CHOICES)
        area = request.POST.getlist("area")
        if area:
            queryset = Order.objects.filter(area__in=area)
        else:
            queryset = Order.objects.all().order_by("-date")
        return render(
            template_name="order/index.html",
            context={"orders": queryset, "filters": filters},
            request=request,
        )


class OrderDetailView(generic.DetailView):
    model = Order
    template_name = "order/detail.html"
    context_object_name = "order"


class OrderUserListView(generic.ListView):
    model = Order
    template_name = "order/userlist.html"
    context_object_name = "orders"

    def get_queryset(self):
        user_id = Client.objects.filter(user_id=self.request.user.id).first()
        return Order.objects.filter(client=user_id).all()


class OrderCreateView(generic.CreateView):
    model = Order
    form_class = OrderCreateForm
    template_name = "order/create.html"
    success_url = "/orders/"

    def form_valid(self, form):
        client = Client.objects.filter(user_id=self.request.user.id).first()
        form.instance.client = client
        form.instance.executor = None
        return super().form_valid(form)


class OrderDeleteView(generic.DeleteView):
    model = Order
    template_name = "order/delete.html"
    success_url = "/orders/userlist/"


class OrderUpdateView(generic.UpdateView):
    model = Order
    form_class = OrderUpdateForm
    template_name = "order/update.html"
    success_url = "/orders/userlist/"
