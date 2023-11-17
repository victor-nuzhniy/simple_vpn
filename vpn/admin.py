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
            self.base_fields["link"].queryset = (
                Page.objects.select_related("personal_site", "personal_site__owner")
                .filter(personal_site__owner=self.instance.page.personal_site.owner)
                .filter(~Q(id__in=[self.instance.page.id]))
            )
            self.fields["link"].queryset = (
                Page.objects.select_related("personal_site", "personal_site__owner")
                .filter(personal_site__owner=self.instance.page.personal_site.owner)
                .filter(~Q(id__in=[self.instance.page.id]))
            )


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

    def get_form(self, request, obj=None, change=False, **kwargs):
        """Change personal_site form field queryset."""
        form = super().get_form(request, obj, change, **kwargs)
        if obj:
            form.base_fields[
                "personal_site"
            ].queryset = PersonalSite.objects.select_related("owner").filter(
                owner=obj.personal_site.owner
            )
        if links := form.base_fields.get("links"):
            links.queryset = (
                Page.objects.select_related("personal_site", "personal_site__owner")
                .filter(
                    personal_site__owner=obj.personal_site.owner,
                )
                .filter(~Q(slug__in=[obj.slug]))
            )
        return form

    def get_queryset(self, request):
        """Upgrade queryset."""
        qs = super().get_queryset(request)
        qs.select_related().only(
            "id",
            "name",
            "slug",
            "sended",
            "loaded",
            "personal_site__id",
            "pesonal_site__name",
            "persona_site__slug",
            "personal_site__owner__username",
            "personal_site__owner__id",
        )
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)


class PageFieldListFilter(admin.SimpleListFilter):
    """Upgraded page field list filter for PageLinksAdmin."""

    title = "page"
    parameter_name = "page"

    def lookups(self, request, model_admin):
        """
        Return a list of tuples.

        The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        queryset = Page.objects.select_related().only(
            "id",
            "name",
            "personal_site__name",
            "personal_site__owner__username",
        )
        return [(page.id, page) for page in queryset]

    def queryset(self, request, queryset):
        """
        Return the filtered queryset.

        Queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        return queryset.filter(page=self.value()) if self.value() else queryset


class LinkFieldListFilter(admin.SimpleListFilter):
    """Upgraded link field list filter for PageLinksAdmin."""

    title = "link"
    parameter_name = "link"

    def lookups(self, request, model_admin):
        """
        Return a list of tuples.

        The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        queryset = Page.objects.select_related().only(
            "id",
            "name",
            "personal_site__name",
            "personal_site__owner__username",
        )
        return [(page.id, page) for page in queryset]

    def queryset(self, request, queryset):
        """
        Return the filtered queryset.

        Queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        return queryset.filter(link=self.value()) if self.value() else queryset


class PageLinksAdmin(admin.ModelAdmin):
    """PageLinks model admin site configuration."""

    list_display = ("id", "page", "link", "quantity")
    list_display_links = ("id", "page", "link", "quantity")
    list_filter = (
        "page__personal_site__owner",
        "page__personal_site",
        PageFieldListFilter,
        LinkFieldListFilter,
    )

    def get_form(self, request, obj=None, change=False, **kwargs):
        """Change personal_site form field queryset."""
        form = super().get_form(request, obj, change, **kwargs)
        if obj:
            form.base_fields["page"].queryset = Page.objects.select_related(
                "personal_site", "personal_site__owner"
            ).filter(personal_site__owner=obj.page.personal_site.owner)
            form.base_fields["link"].queryset = Page.objects.select_related(
                "personal_site", "personal_site__owner"
            ).filter(personal_site__owner=obj.page.personal_site.owner)
        return form


admin.site.register(PersonalSite, PersonalSiteAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(PageLinks, PageLinksAdmin)
