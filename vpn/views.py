"""Class and function views for vpn app."""
from typing import Dict

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.db.models import Prefetch, QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    TemplateView,
    UpdateView,
)

from vpn.forms import (
    CustomAuthForm,
    CustomPasswordChangeForm,
    CustomUserCreationForm,
    PageCreateForm,
    PersonalSiteCreateForm,
    UserAccountForm,
)
from vpn.mixins import ChangeSuccessURLMixin, CustomUserPassesTestMixin
from vpn.models import Page, PageLinks, PersonalSite
from vpn.utils import add_link_quantity_and_request_content_length, get_links


class IndexView(TemplateView):
    """Index view."""

    template_name = "vpn/index.html"
    extra_context = {"title": "Welcome"}


class RegisterView(ChangeSuccessURLMixin, FormView):
    """View for user registration."""

    form_class = CustomUserCreationForm
    template_name = "vpn/auth/user_creation_form.html"
    extra_context = {"title": "Sign up"}
    success_url = reverse_lazy("vpn:sign_up")

    def form_valid(self, form: CustomUserCreationForm) -> HttpResponseRedirect:
        """Create new user and login."""
        user: User = form.save()
        login(self.request, user)
        return super().form_valid(form)


class CustomLoginView(ChangeSuccessURLMixin, LoginView):
    """Login view."""

    extra_context = {"title": "Sign in"}
    next_page = "vpn:sign_up"
    redirect_authenticated_user = True
    template_name = "vpn/auth/login.html"
    form_class = CustomAuthForm


class CustomPasswordChangeView(ChangeSuccessURLMixin, PasswordChangeView):
    """Class view for user password changing."""

    success_url = reverse_lazy("vpn:signup")
    template_name = "vpn/auth/password_change.html"
    extra_context = {"title": "Password change"}
    form_class = CustomPasswordChangeForm


class AccountView(CustomUserPassesTestMixin, ChangeSuccessURLMixin, UpdateView):
    """Update user information."""

    model = User
    form_class = UserAccountForm
    template_name = "vpn/account.html"
    extra_context = {"title": "Personal info"}
    success_url = reverse_lazy("vpn:sign_up")

    def get_context_data(self, **kwargs) -> Dict:
        """Get context data."""
        context = super().get_context_data(**kwargs)
        context["personal_sites"] = PersonalSite.objects.filter(owner=self.request.user)
        context["pages"] = (
            Page.objects.select_related()
            .only(
                "name",
                "slug",
                "sended",
                "loaded",
                "personal_site__name",
                "personal_site__slug",
                "personal_site__owner__username",
            )
            .prefetch_related(
                Prefetch(
                    "page_links",
                    queryset=PageLinks.objects.select_related().only(
                        "quantity",
                        "link",
                        "page__id",
                        "page__name",
                        "page__personal_site__slug",
                        "page__personal_site__name",
                        "page__personal_site__owner__id",
                        "page__personal_site__owner__username",
                    ),
                )
            )
            .filter(personal_site__owner__id=self.request.user.id)
        )
        return context


class CreateSiteView(LoginRequiredMixin, ChangeSuccessURLMixin, FormView):
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


class UpdateSiteView(CustomUserPassesTestMixin, ChangeSuccessURLMixin, UpdateView):
    """Update site view."""

    form_class = PersonalSiteCreateForm
    template_name = "vpn/personal_site/update_personal_site.html"
    extra_context = {"title": "Update site"}
    success_url = reverse_lazy("vpn:sign_up")

    def get_queryset(self):
        """Return queryset using current user."""
        return PersonalSite.objects.filter(owner=self.request.user)


class DeleteSiteView(CustomUserPassesTestMixin, ChangeSuccessURLMixin, DeleteView):
    """Delete PersonalSite model instance."""

    model = PersonalSite
    template_name = "vpn/personal_site/delete_personal_site.html"
    extra_context = {"title": "Delete site"}
    success_url = reverse_lazy("vpn:sign_up")

    def get_queryset(self):
        """Return queryset using current user."""
        return PersonalSite.objects.filter(owner=self.request.user)


class CreatePageView(LoginRequiredMixin, ChangeSuccessURLMixin, CreateView):
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


class UpdatePageView(CustomUserPassesTestMixin, ChangeSuccessURLMixin, UpdateView):
    """Update Page model instance."""

    form_class = PageCreateForm
    template_name = "vpn/page/update_page.html"
    extra_context = {"title": "Update page"}
    success_url = reverse_lazy("vpn:sign_up")

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


class DeletePageView(CustomUserPassesTestMixin, ChangeSuccessURLMixin, DeleteView):
    """Delete Page model instance."""

    model = Page
    template_name = "vpn/page/delete_page.html"
    extra_context = {"title": "Delete page"}
    success_url = reverse_lazy("vpn:sign_up")

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
        if self.request.site.id == 2:
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
        if self.request.site.id == 2:
            response.headers["page_id"] = context["page"].id
        return response
