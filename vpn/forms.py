"""Forms for vpn app."""
from django import forms

from vpn.models import PersonalSite


class PersonalSiteForm(forms.ModelForm):
    """Form for PersonalSite model."""

    class Meta:
        """Class Meta for PersonalSiteForm."""

        model = PersonalSite
        fields = ("name", "slug")
