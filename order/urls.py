from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("", views.OrderIndexListView.as_view(), name="index"),
    path("<int:pk>/update", views.OrderUpdateView.as_view(), name="update"),
    path("<int:pk>/delete", views.OrderDeleteView.as_view(), name="delete"),
    path("<int:pk>/offers", views.OrderOffersListView.as_view(), name="offers"),
    path("create/", views.OrderCreateView.as_view(), name="create"),
    path("user_list/", views.OrderUserListView.as_view(), name="userlist"),
]
