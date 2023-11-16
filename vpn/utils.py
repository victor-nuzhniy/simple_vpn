"""Utitlites for vpn app."""
from django.db.models import F, QuerySet
from django.http import HttpRequest

from vpn.models import Page, PageLinks


def add_link_quantity(request: HttpRequest, page: Page) -> None:
    """Perform increase link quantity usage."""
    referer_list = request.META.get("HTTP_REFERER").split("/")
    ref_page = Page.objects.filter(
        slug=referer_list[-2], personal_site__slug=referer_list[-3]
    ).first()
    if ref_page:
        if page_links := PageLinks.objects.filter(page=ref_page, link=page).first():
            page_links.quantity = F("quantity") + 1
            page_links.save()


def get_links(page: Page) -> QuerySet:
    """Get Page queryset with linkable instances."""
    ids = [link.link.id for link in PageLinks.objects.filter(page=page)]
    return Page.objects.select_related("personal_site").filter(id__in=ids)
