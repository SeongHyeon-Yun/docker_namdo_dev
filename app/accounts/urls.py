from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_page, name="logout"),
    path("join/", views.join_page, name="join"),
    path("join_check/", views.join_check_page, name="join_check"),
    path("id_search/", views.id_search, name="id_search"),
    path("pw_search/", views.pw_search, name="pw_search"),
    path("pw_change/", views.pw_change, name="pw_change"),
    path("pw_search_result/", views.pw_search_result, name="pw_search_result"),
]
