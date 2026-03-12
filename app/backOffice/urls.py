from django.urls import path
from . import views


app_name = "back_office"

urlpatterns = [
    path("", views.index, name="index"),
    path("item_page/", views.item_page, name="item_page"),
    path("order_page/", views.order_page, name="order_page"),
    path("delivery_page/", views.delivery_page, name="delivery_page"),
    path("wallet_page/", views.wallet_page, name="wallet_page"),
    path("user_page/", views.user_page, name="user_page"),
    path("api/wallet-count/", views.wallet_count_api, name="wallet_count_api"),
]
