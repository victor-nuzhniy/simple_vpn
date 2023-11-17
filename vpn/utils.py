"""Utitlites for vpn app."""
from django.db.models import F, QuerySet
from django.http import HttpRequest

from vpn.models import Page, PageLinks


def add_link_quantity_and_request_content_length(
    request: HttpRequest, page: Page
) -> None:
    """Perform increase link quantity usage."""
    if referer := request.META.get("HTTP_REFERER"):
        referer_list = referer.split("/")
        ref_page = Page.objects.filter(
            slug=referer_list[-2], personal_site__slug=referer_list[-3]
        ).first()
        if ref_page:
            if page_links := PageLinks.objects.filter(page=ref_page, link=page).first():
                page_links.quantity = F("quantity") + 1
                page_links.save()
            content_length = request.headers.get("Content-Length")
            ref_page.loaded = F("loaded") + len(content_length)
            ref_page.save()


def get_links(page: Page) -> QuerySet:
    """Get Page queryset with linkable instances."""
    queryset = PageLinks.objects.filter(page=page).select_related().only("page__id")
    ids = [link.link.id for link in queryset]
    return Page.objects.select_related("personal_site").filter(id__in=ids)
