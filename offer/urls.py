from django.urls import path

from . import views

app_name = "offers"

urlpatterns = [
    path("", views.OfferIndexListView.as_view(), name="index"),
    path("<int:order_id>/make", views.OfferCreateView.as_view(), name="make"),
    path("<int:offer_id>/order", views.OfferOrderListView.as_view(), name="orders"),
]
