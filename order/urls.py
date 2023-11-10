from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("", views.OrderIndexView.as_view(), name="index"),
    path("<int:pk>/", views.OrderDetailView.as_view(), name="detail"),
    path("userlist/", views.OrderUserListView.as_view(), name="userlist"),
    path("create/", views.OrderCreateView.as_view(), name="create"),
    path("<int:pk>/delete", views.OrderDeleteView.as_view(), name="delete"),
    path("<int:pk>/update", views.OrderUpdateView.as_view(), name="update"),
]
