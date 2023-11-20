from django.db import transaction
from django.db.utils import IntegrityError
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import generic

from order.models import Order
from variables.choices import Statuses
from variables.mixins import OrderOfferClientContentMixin

from .forms import OfferCreateForm
from .models import Offer


class OfferCreateView(OrderOfferClientContentMixin, generic.CreateView):
    model = Offer
    form_class = OfferCreateForm
    template_name = "offers/create.html"
    success_url = reverse_lazy("orders:index")

    def form_valid(self, form):
        executor = self.client
        order_id = self.kwargs["order_id"]
        form.instance.executor = executor
        form.instance.order_id = order_id
        try:
            return super().form_valid(form)
        except IntegrityError:
            error_message = "Offer for this order already exists."
            return render(
                self.request, self.template_name, {"form": form, "error": error_message}
            )


class OfferIndexListView(OrderOfferClientContentMixin, generic.ListView):
    template_name = "offers/index.html"

    def get_queryset(self):
        match self.request.GET.get("status"):
            case "in_progress":
                return Offer.objects.filter(
                    executor=self.client, status=Statuses.IN_PROGRESS
                ).all()
            case "done":
                return Offer.objects.filter(
                    executor=self.client, status=Statuses.DONE
                ).all()
            case "pending":
                return Offer.objects.filter(
                    executor=self.client, status=Statuses.PENDING
                ).all()
            case "declined":
                return Offer.objects.filter(
                    executor=self.client, status=Statuses.DECLINED
                ).all()
            case "under_approval":
                return Offer.objects.filter(
                    executor=self.client, status=Statuses.UNDER_APPROVAL
                ).all()
            case _:
                return (
                    Offer.objects.filter(executor=self.client).order_by("-status").all()
                )

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        order = Order.objects.filter(id=request.POST.get("order_id")).first()
        offer = Offer.objects.filter(id=request.POST.get("offer_id")).first()
        match order.status:
            case Statuses.IN_PROGRESS:
                offer.status = Statuses.UNDER_APPROVAL
                offer.save()
                url = reverse("offers:index") + "?status=under_approval"
                return redirect(url)
            case Statuses.UNDER_APPROVAL:
                offer.status = Statuses.DONE
                order.status = Statuses.DONE
                offer.save()
                order.save()
                url = reverse("offers:index") + "?status=done"
                return redirect(url)


class OfferOrderListView(OrderOfferClientContentMixin, generic.ListView):
    template_name = "offers/order_list.html"
    context_object_name = "offer"

    def get_queryset(self, **kwargs):
        offer_id = self.kwargs.get("offer_id")
        return Offer.objects.filter(pk=offer_id).filter(status="In progress").first()
