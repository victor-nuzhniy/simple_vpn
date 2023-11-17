"""Forms for vpn app."""
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    UserCreationForm,
)
from django.contrib.auth.models import User
from django.db.models import Q

from vpn.models import Page, PersonalSite


class PersonalSiteCreateForm(forms.ModelForm):
    """Form for PersonalSite model instance creation."""

    def __init__(self, *args, **kwargs):
        """Rewrite fields styling."""
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs["class"] = "custom-input custom-input-height"
        self.fields["slug"].widget.attrs["class"] = "custom-input custom-input-height"

    class Meta:
        """Class Meta for PersonalSiteCreateForm."""

        model = PersonalSite
        fields = ("name", "slug")


class PageCreateForm(forms.ModelForm):
    """Form for Page model instance creation."""

    class Meta:
        """Class Meta for PageCreateForm."""

        model = Page
        exclude = ("sended", "loaded")

    def __init__(self, *args, **kwargs) -> None:
        """Customize personal_site and links fields querysets."""
        owner = kwargs.pop("owner", None)
        slug = kwargs.pop("slug", None)
        super(PageCreateForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs["class"] = "custom-input custom-input-height"
        self.fields["slug"].widget.attrs["class"] = "custom-input custom-input-height"
        self.fields["personal_site"].widget.attrs[
            "class"
        ] = "custom-input custom-input-height"
        self.fields["content"].widget.attrs[
            "class"
        ] = "custom-input custom-input-height"
        self.fields["links"].widget.attrs["class"] = "custom-input"
        if owner:
            personal_site_queryset = (
                PersonalSite.objects.filter(owner=owner)
                .select_related()
                .only("name", "slug", "owner__username")
            )
            links_queryset = (
                Page.objects.filter(personal_site__owner=owner)
                .select_related()
                .only(
                    "name",
                    "personal_site__name",
                    "personal_site__owner__username",
                )
            )
            if slug:
                links_queryset = links_queryset.filter(~Q(slug__in=[slug]))
            self.fields["personal_site"].queryset = personal_site_queryset
            self.fields["links"].queryset = links_queryset


class UserAccountForm(forms.ModelForm):
    """Form for User model."""

    class Meta:
        """Class Meta for UserAccountForm."""

        model = User
        fields = ("username", "email", "first_name", "last_name")

    def __init__(self, *args, **kwargs) -> None:
        """Rewrite fields class."""
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs[
            "class"
        ] = "custom-input custom-input-height"
        self.fields["email"].widget.attrs["class"] = "custom-input custom-input-height"
        self.fields["first_name"].widget.attrs[
            "class"
        ] = "custom-input custom-input-height"
        self.fields["last_name"].widget.attrs[
            "class"
        ] = "custom-input custom-input-height"


class CustomAuthForm(AuthenticationForm):
    """Customize AuthenticationForm fields classes."""

    def __init__(self, *args, **kwargs) -> None:
        """Restyle fields classes."""
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs[
            "class"
        ] = "custom-input custom-input-height"
        self.fields["password"].widget.attrs[
            "class"
        ] = "custom-input custom-input-height"


class CustomUserCreationForm(UserCreationForm):
    """Customize UserCreationForm fields."""

    def __init__(self, *args, **kwargs) -> None:
        """Restyle fields classes."""
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs[
            "class"
        ] = "custom-input custom-input-height"
        self.fields["password1"].widget.attrs[
            "class"
        ] = "custom-input custom-input-height"
        self.fields["password2"].widget.attrs[
            "class"
        ] = "custom-input custom-input-height"


class CustomPasswordChangeForm(PasswordChangeForm):
    """Customize PasswordChangeForm fields."""

    def __init__(self, *args, **kwargs) -> None:
        """Restyle fields classes."""
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget.attrs[
            "class"
        ] = "custom-input custom-input-height"
        self.fields["new_password1"].widget.attrs[
            "class"
        ] = "custom-input custom-input-height"
        self.fields["new_password2"].widget.attrs[
            "class"
        ] = "custom-input custom-input-height"
