"""Admin site configuration for vpn app."""
from django import forms
from django.contrib import admin
from django.db.models import Q

from vpn.models import Page, PageLinks, PersonalSite


class PageLinksInlineForm(forms.ModelForm):
    """Rewrite PageLinksInlineForm link field queryset."""

    def __init__(self, *args, **kwargs):
        """Rewrite init method PageLinksInlineForm."""
        super().__init__(*args, **kwargs)
        if "instance" in kwargs:
            self.base_fields["link"].queryset = Page.objects.filter(
                personal_site__owner=self.instance.page.personal_site.owner
            ).filter(~Q(id__in=[self.instance.page.id]))


class PageLinksInline(admin.StackedInline):
    """Inline PageLinks admin site configuration."""

    model = PageLinks
    form = PageLinksInlineForm
    extra = 1
    fk_name = "page"


class PersonalSiteAdmin(admin.ModelAdmin):
    """PersonalSite model admin site configuration."""

    list_display = ("id", "owner", "name", "slug")
    list_display_links = ("id", "owner", "name", "slug")
    list_filter = ("owner",)


class PageAdmin(admin.ModelAdmin):
    """Page model admin site configuration."""

    list_display = ("id", "name", "slug", "personal_site", "sended", "loaded")
    list_display_links = ("id", "name", "personal_site", "sended", "loaded")
    list_filter = ("personal_site",)
    inlines = [PageLinksInline]

    def get_form(self, request, obj=None, change=False, **kwargs):
        """Change personal_site form field queryset."""
        form = super().get_form(request, obj, change, **kwargs)
        form.base_fields["personal_site"].queryset = PersonalSite.objects.filter(
            owner=obj.personal_site.owner
        )
        if links := form.base_fields.get("links"):
            links.queryset = Page.objects.filter(
                personal_site__owner=obj.personal_site.owner,
            ).filter(~Q(slug__in=[obj.slug]))
        return form


class PageLinksAdmin(admin.ModelAdmin):
    """PageLinks model admin site configuration."""

    list_display = ("id", "page", "link", "quantity")
    list_display_links = ("id", "page", "link", "quantity")
    list_filter = ("page", "link")


admin.site.register(PersonalSite, PersonalSiteAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(PageLinks, PageLinksAdmin)
