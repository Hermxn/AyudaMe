from django.http import Http404
from django.shortcuts import get_object_or_404, redirect

from offer.models import Offer
from order.models import Client, Order
from variables import choices


class OrderOfferClientContentMixin:
    def __init__(self):
        self.client = None
        self.client_orders = None
        self.client_offers = None
        self.object_list = None
        self.filters_area = choices.AREA_CHOICES

    def _get_client_data(self, request):
        try:
            self.client = get_object_or_404(Client, user=request.user.id)
            self.client_orders = Order.objects.filter(client=self.client).all()
            self.client_offers = Offer.objects.filter(executor=self.client).all()
        except Http404:
            return redirect("/")

    def get(self, request, *args, **kwargs):
        self._get_client_data(request)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self._get_client_data(request)
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client_orders"] = self.client_orders
        context["client_offers"] = self.client_offers
        context["filters_area"] = self.filters_area
        return context
