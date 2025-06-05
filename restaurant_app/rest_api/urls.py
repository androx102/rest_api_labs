from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  
    TokenRefreshView,
    TokenBlacklistView,
)




urlpatterns = [
    #path("auth/register", views.RegisterEndpoint.as_view(), name="sign_up"),
    path("auth/login", TokenObtainPairView.as_view(), name="sign_in"),
    #path("auth/refresh", TokenRefreshView.as_view(), name="ref_token"),
    #path("auth/logout", TokenBlacklistView.as_view(), name="logout"),

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