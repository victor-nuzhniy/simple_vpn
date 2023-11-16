"""Forms for vpn app."""
from django import forms
from django.db.models import Q

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
        exclude = ("sended", "loaded")

    def __init__(self, *args, **kwargs) -> None:
        """Customize personal_site and links fields querysets."""
        owner = kwargs.pop("owner", None)
        slug = kwargs.pop("slug", None)
        super(PageCreateForm, self).__init__(*args, **kwargs)
        if owner:
            personal_site_queryset = PersonalSite.objects.filter(owner=owner)
            links_queryset = Page.objects.filter(
                personal_site__owner=owner
            ).select_related("personal_site")
            if slug:
                links_queryset = links_queryset.filter(~Q(slug__in=[slug]))
            self.fields["personal_site"].queryset = personal_site_queryset
            self.fields["links"].queryset = links_queryset
