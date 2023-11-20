from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import generic

from offer.models import Offer
from variables.choices import Statuses
from variables.mixins import OrderOfferClientContentMixin

from .forms import OrderCreateForm, OrderUpdateForm
from .models import Order


class OrderIndexListView(OrderOfferClientContentMixin, generic.ListView):
    template_name = "order/index.html"
    context_object_name = "orders"

    def get_queryset(self):
        queryset = (
            Order.objects.filter(status=Statuses.PENDING)
            .exclude(client=self.client)
            .order_by("-date")
        )
        area = self.request.POST.getlist("area")
        if area:
            queryset = queryset.filter(area__in=area).all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders_with_offer = [offer.order for offer in self.client_offers]
        context["orders_with_offer"] = orders_with_offer
        return context

    def post(self, request, *args, **kwargs):
        self.get(request, *args, **kwargs)
        context = self.get_context_data()
        context["orders"] = self.get_queryset()
        return render(
            template_name="order/index.html",
            context=context,
            request=request,
        )


class OrderUserListView(OrderOfferClientContentMixin, generic.ListView):
    model = Order
    template_name = "order/user_orders_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        match self.request.GET.get("status"):
            case "in_work":
                return (
                    Order.objects.filter(
                        client=self.client, status=Statuses.IN_PROGRESS
                    )
                    .all()
                    .order_by("-date")
                )
            case "done":
                return (
                    Order.objects.filter(client=self.client, status=Statuses.DONE)
                    .all()
                    .order_by("-date")
                )
            case "pending":
                return (
                    Order.objects.filter(client=self.client, status=Statuses.PENDING)
                    .all()
                    .order_by("-date")
                )
            case "under_approval":
                return (
                    Order.objects.filter(
                        client=self.client, status=Statuses.UNDER_APPROVAL
                    )
                    .all()
                    .order_by("-date")
                )
            case _:
                return Order.objects.filter(client=self.client).order_by("-date")

    transaction.atomic()

    def post(self, request, *args, **kwargs):
        order = Order.objects.filter(id=request.POST.get("order_id")).first()
        offer = Offer.objects.filter(id=request.POST.get("offer_id")).first()
        match offer.status:
            case Statuses.IN_PROGRESS:
                order.status = Statuses.UNDER_APPROVAL
                order.save()
                url = reverse("orders:userlist") + "?status=under_approval"
                return redirect(url)
            case Statuses.UNDER_APPROVAL:
                order.status = Statuses.DONE
                offer.status = Statuses.DONE
                order.save()
                offer.save()
                url = reverse("orders:userlist") + "?status=done"
                return redirect(url)


class OrderCreateView(OrderOfferClientContentMixin, generic.CreateView):
    model = Order
    form_class = OrderCreateForm
    template_name = "order/create.html"
    success_url = "/orders/user_list/"

    def form_valid(self, form):
        form.instance.client = self.client
        form.instance.executor = None
        return super().form_valid(form)


class OrderDeleteView(OrderOfferClientContentMixin, generic.DeleteView):  # type: ignore
    model = Order
    template_name = "order/delete.html"
    success_url = "/orders/user_list/"


class OrderUpdateView(OrderOfferClientContentMixin, generic.UpdateView):
    model = Order
    form_class = OrderUpdateForm
    template_name = "order/update.html"
    success_url = "/orders/user_list/"


class OrderOffersListView(OrderOfferClientContentMixin, generic.ListView):
    template_name = "order/offers_list.html"

    def get_queryset(self, **kwargs):
        order = Order.objects.filter(id=self.kwargs["pk"]).first()
        if order.offer:
            return (
                Offer.objects.filter(id=order.offer)
                .exclude(status=Statuses.DECLINED)
                .all()
            )
        return (
            Offer.objects.filter(order=self.kwargs["pk"])
            .exclude(status=Statuses.DECLINED)
            .all()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order"] = Order.objects.get(pk=self.kwargs["pk"])
        context["client"] = self.client
        context["phone"] = self.client.phone
        return context

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        order = Order.objects.filter(id=request.POST.get("order_id")).first()
        offer = Offer.objects.filter(id=request.POST.get("offer_id")).first()
        if "accept" in request.POST:
            order.offer = request.POST.get("offer_id")
            order.executor = offer.executor
            order.status = Statuses.IN_PROGRESS
            offer.status = Statuses.IN_PROGRESS
            order.save()
            offer.save()
        elif "declined" in request.POST:
            offer.status = Statuses.DECLINED
            offer.save()
        return redirect(request.path)
