"""Forms for vpn app."""
from django import forms

from vpn.models import Page, PersonalSite


class PersonalSiteCreateForm(forms.ModelForm):
    """Form for PersonalSite model instance creation."""

    class Meta:
        """Class Meta for PersonalSiteCreateForm."""

        model = PersonalSite
        fields = ("name", "slug")


class PageCreateForm(forms.ModelForm):
    """Form for Page model instance creation."""

    class Meta:
        """Class Meta for PageCreateForm."""

        model = Page
        fields = "__all__"

    def __init__(self, *args, **kwargs) -> None:
        """Customize personal_site and links fields querysets."""
        owner = kwargs.pop("owner")
        super(PageCreateForm, self).__init__(*args, **kwargs)
        if owner:
            self.fields["personal_site"].queryset = PersonalSite.objects.filter(
                owner=owner
            )
            self.fields["links"].queryset = Page.objects.filter(
                personal_site__owner=owner
            )
