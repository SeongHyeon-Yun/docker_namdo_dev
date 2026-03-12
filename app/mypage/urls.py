from django.urls import path
from . import views

app_name = "mypage"

urlpatterns = [
    path("", views.mypage, name="index"),
    path("deposit/", views.deposit, name="deposit"),
    path("refund/", views.refund, name="refund"),
    path("amount_list/", views.amount, name="amount"),
]
