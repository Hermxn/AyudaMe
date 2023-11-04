from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from variables import choices

from .models import Order


class IndexView(generic.ListView):
    template_name = "order/index.html"
    ordering = ["-rating"]
    queryset = Order.objects.all()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data()
        context["orders"] = Order.objects.all()
        context["filters"] = list(choices.AREA_CHOICES)
        return context

    @staticmethod
    def post(request: HttpRequest) -> HttpResponse:
        filters = list(choices.AREA_CHOICES)
        area = request.POST.getlist("area")
        if area:
            queryset = Order.objects.filter(area__in=area)
        else:
            queryset = Order.objects.all().order_by("-rating")
        return render(
            template_name="order/index.html",
            context={"orders": queryset, "filters": filters},
            request=request,
        )


class DetailView(generic.DetailView):
    model = Order
    template_name = "orders/detail.html"
    context_object_name = "order"
