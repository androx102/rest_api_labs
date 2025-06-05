from django.urls import path
from . import views

urlpatterns = [
    path(
        "menu/",
        views.MenuItems.as_view(),
        name="menu",
    ),
    path(
        "menu/<str:pk>",
        views.MenuItems.as_view(),
        name="menu_uuid",
    ),
    path(
        "orders/",
        views.Orders.as_view(),
        name="order",
    ),
    path(
        "orders/<str:pk>",
        views.Orders.as_view(),
        name="order",
    ),


]