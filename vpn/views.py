"""Class and function views for vpn app."""
from abc import ABC

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, UpdateView

from vpn.models import PersonalSite


class RegisterView(FormView):
    """View for user registration."""

    form_class = UserCreationForm
    template_name = "vpn/user_creation_form.html"
    extra_context = {"title": "Sign up"}
    success_url = reverse_lazy("vpn:sign_up")

    def form_valid(self, form: UserCreationForm) -> HttpResponseRedirect:
        """Create new user and login."""
        user: User = form.save()
        login(self.request, user)
        return super().form_valid(form)


class CustomLoginView(LoginView):
    """Login view."""

    extra_context = {"title": "Sign in"}
    next_page = "vpn:sign_up"
    redirect_authenticated_user = True
    template_name = "vpn/login.html"


class CustomPasswordChangeView(PasswordChangeView):
    """Class view for user password changing."""

    success_url = reverse_lazy("vpn:signup")  # TODO for changing
    template_name = "vpn/password_change.html"
    extra_context = {"title": "Password change"}


class AccountView(UserPassesTestMixin, UpdateView, ABC):
    """Update user information."""

    model = User
    fields = ("username", "email", "first_name", "last_name")
    template_name = "vpn/account.html"
    extra_context = {"title": "Personal info"}
    success_url = reverse_lazy("vpn:sign_up")

    def test_func(self) -> bool:
        """Test whether user is user."""
        if self.request.user.is_anonymous:
            return False
        return self.request.user.pk == self.kwargs.get("pk")


class CreateSiteView(CreateView):
    """Create site view."""

    model = PersonalSite
    fields = ("owner", "name")
    template_name = "vpn/create_personal_site.html"
