"""Urls for vpn app."""
from django.contrib.auth.views import LogoutView
from django.urls import path

from vpn.views import (
    AccountView,
    CreatePageView,
    CreateSiteView,
    CustomLoginView,
    CustomPasswordChangeView,
    DeletePageView,
    DeleteSiteView,
    IndexView,
    PageView,
    RegisterView,
    UpdatePageView,
    UpdateSiteView,
)

app_name = "vpn"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("sign-up/", RegisterView.as_view(), name="sign_up"),
    path("sign-in/", CustomLoginView.as_view(), name="sign_in"),
    path("logout/", LogoutView.as_view(next_page="vpn:index"), name="logout"),
    path(
        "password-change/", CustomPasswordChangeView.as_view(), name="password_change"
    ),
    path("account/<int:pk>/", AccountView.as_view(), name="account"),
    path("create-site/", CreateSiteView.as_view(), name="create_site"),
    path(
        "update-site/<int:owner_id>/<str:slug>/",
        UpdateSiteView.as_view(),
        name="update_site",
    ),
    path(
        "delete-site/<int:owner_id>/<str:slug>/",
        DeleteSiteView.as_view(),
        name="delete_site",
    ),
    path(
        "create-page/",
        CreatePageView.as_view(),
        name="create_page",
    ),
    path(
        "update-page/<int:owner_id>/<str:site_slug>/<str:slug>/",
        UpdatePageView.as_view(),
        name="update_page",
    ),
    path(
        "delete-page/<int:owner_id>/<str:site_slug>/<str:slug>/",
        DeletePageView.as_view(),
        name="delete_page",
    ),
    path("<str:site_slug>/<str:slug>/", PageView.as_view(), name="page"),
]
