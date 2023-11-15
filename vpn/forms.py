"""Forms for vpn app."""
from django import forms


class PersonalSiteForm(forms.Form):
    """Form for PersonalSite model."""

    name = forms.CharField(max_length=100, label="Site name")
