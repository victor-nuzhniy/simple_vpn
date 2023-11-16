"""Class and function views for vpn app."""
from abc import ABC
from typing import Dict

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.db.models import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    UpdateView,
)

from vpn.forms import PageCreateForm, PersonalSiteCreateForm
from vpn.models import Page, PersonalSite
from vpn.utils import add_link_quantity_and_request_content_length, get_links


class RegisterView(FormView):
    """View for user registration."""

    form_class = UserCreationForm
    template_name = "vpn/auth/user_creation_form.html"
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
    template_name = "vpn/auth/login.html"


class CustomPasswordChangeView(PasswordChangeView):
    """Class view for user password changing."""

    success_url = reverse_lazy("vpn:signup")  # TODO for changing
    template_name = "vpn/auth/password_change.html"
    extra_context = {"title": "Password change"}


class AccountView(UserPassesTestMixin, UpdateView, ABC):
    """Update user information."""

    model = User
    fields = ("username", "email", "first_name", "last_name")
    template_name = "vpn/account.html"
    extra_context = {"title": "Personal info"}
    success_url = reverse_lazy("vpn:sign_up")

    def get_context_data(self, **kwargs) -> Dict:
        """Get context data."""
        context = super().get_context_data(**kwargs)
        context["personal_sites"] = PersonalSite.objects.filter(owner=self.request.user)
        context["pages"] = (
            Page.objects.select_related("personal_site")
            .prefetch_related("page_links")
            .filter(personal_site__owner=self.request.user)
        )

        return context

    def test_func(self) -> bool:
        """Test whether user is user."""
        if self.request.user.is_anonymous:
            return False
        return self.request.user.pk == self.kwargs.get("pk")


class CreateSiteView(LoginRequiredMixin, FormView):
    """Create site view."""

    form_class = PersonalSiteCreateForm
    template_name = "vpn/personal_site/create_personal_site.html"
    extra_context = {"title": "Create site"}
    success_url = reverse_lazy("vpn:sign_up")

    def form_valid(self, form) -> HttpResponseRedirect:
        """Create personal site."""
        data: Dict = form.cleaned_data
        PersonalSite(**data, owner=self.request.user).save()
        return super().form_valid(form)


class UpdateSiteView(UserPassesTestMixin, UpdateView, ABC):
    """Update site view."""

    model = PersonalSite
    fields = ("name", "slug")
    template_name = "vpn/personal_site/update_personal_site.html"
    extra_context = {"title": "Update site"}
    success_url = reverse_lazy("vpn:sign_up")

    def test_func(self) -> bool:
        """Test whether user is user."""
        if self.request.user.is_anonymous:
            return False
        return self.request.user.pk == self.kwargs.get("owner_id")

    def get_queryset(self):
        """Return queryset using current user."""
        return PersonalSite.objects.filter(owner=self.request.user)


class DeleteSiteView(UserPassesTestMixin, DeleteView, ABC):
    """Delete PersonalSite model instance."""

    model = PersonalSite
    template_name = "vpn/personal_site/delete_personal_site.html"
    extra_context = {"title": "Delete site"}
    success_url = reverse_lazy("vpn:sign_up")

    def test_func(self) -> bool:
        """Test whether user is user."""
        if self.request.user.is_anonymous:
            return False
        return self.request.user.pk == self.kwargs.get("owner_id")

    def get_queryset(self):
        """Return queryset using current user."""
        return PersonalSite.objects.filter(owner=self.request.user)


class CreatePageView(LoginRequiredMixin, CreateView):
    """Create Page model instance."""

    form_class = PageCreateForm
    template_name = "vpn/page/create_page.html"
    extra_context = {"title": "Create page"}
    success_url = reverse_lazy("vpn:sign_up")

    def get_form_kwargs(self):
        """Set 'owner' kwarg argument to form kwargs."""
        kwargs = super().get_form_kwargs()
        kwargs.update({"owner": self.request.user})
        return kwargs


class UpdatePageView(UserPassesTestMixin, UpdateView, ABC):
    """Update Page model instance."""

    form_class = PageCreateForm
    template_name = "vpn/page/update_page.html"
    extra_context = {"title": "Update page"}
    success_url = reverse_lazy("vpn:sign_up")

    def test_func(self) -> bool:
        """Test whether user is user."""
        if self.request.user.is_anonymous:
            return False
        return self.request.user.pk == self.kwargs.get("owner_id")

    def get_form_kwargs(self):
        """Set 'owner' kwarg argument to form kwargs."""
        kwargs = super().get_form_kwargs()
        kwargs.update({"owner": self.request.user, "slug": self.kwargs.get("slug")})
        return kwargs

    def get_queryset(self):
        """Return queryset using current user."""
        return Page.objects.filter(
            personal_site__owner=self.request.user,
            personal_site__slug=self.kwargs.get("site_slug"),
        )


class DeletePageView(UserPassesTestMixin, DeleteView, ABC):
    """Delete Page model instance."""

    model = Page
    template_name = "vpn/page/delete_page.html"
    extra_context = {"title": "Delete page"}
    success_url = reverse_lazy("vpn:sign_up")

    def test_func(self) -> bool:
        """Test whether user is user."""
        if self.request.user.is_anonymous:
            return False
        return self.request.user.pk == self.kwargs.get("owner_id")

    def get_queryset(self):
        """Return queryset using current user."""
        return Page.objects.filter(
            personal_site__owner=self.request.user,
            personal_site__slug=self.kwargs.get("site_slug"),
        )


class PageView(DetailView):
    """Get Page model instance."""

    model = Page
    template_name = "vpn/page/page.html"
    context_object_name = "page"

    def get_context_data(self, **kwargs) -> Dict:
        """Get context data."""
        context = super().get_context_data(**kwargs)
        page = context["page"]
        context["title"] = page.name
        context["links"] = get_links(page)
        add_link_quantity_and_request_content_length(self.request, page)
        return context

    def get_queryset(self) -> QuerySet:
        """Get Page queryset using personal site slug."""
        return Page.objects.select_related("personal_site").filter(
            personal_site__slug=self.kwargs.get("site_slug")
        )

    def render_to_response(self, context, **response_kwargs) -> HttpResponse:
        """Add header with page id."""
        response = super().render_to_response(context, **response_kwargs)
        response.headers["page_id"] = context["page"].id
        return response
