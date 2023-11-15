"""Admin site configuration for vpn app."""
from django.contrib import admin

from vpn.models import Page, PageLinks, PersonalSite


class PersonalSiteAdmin(admin.ModelAdmin):
    """PersonalSite model admin site configuration."""

    list_display = ("id", "owner", "name", "slug")
    list_display_links = ("id", "owner", "name", "slug")
    list_filter = ("owner",)


class PageAdmin(admin.ModelAdmin):
    """Page model admin site configuration."""

    list_display = ("id", "name", "personal_site", "sended", "loaded")
    list_display_links = ("id", "name", "personal_site", "sended", "loaded")
    list_filter = ("personal_site",)


class PageLinksAdmin(admin.ModelAdmin):
    """PageLinks model admin site configuration."""

    list_display = ("id", "page", "link", "quantity")
    list_display_links = ("id", "page", "link", "quantity")
    list_filter = ("page", "link")


admin.site.register(PersonalSite, PersonalSiteAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(PageLinks, PageLinksAdmin)
