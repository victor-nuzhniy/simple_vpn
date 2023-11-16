"""Custom vpn app midleware."""
from django.db.models import F

from vpn.models import Page


class ContentLengthMiddleware:
    """Mixin for adding response content length to Page sended field."""

    def __init__(self, get_response):
        """Initialize middleware."""
        self.get_response = get_response

    def __call__(self, request):
        """Call middleware functionality."""
        response = self.get_response(request)

        if page_id := response.headers.pop("page_id", None):
            page = Page.objects.get(id=int(page_id[1]))
            page.sended = F("sended") + int(response.headers.get("Content-Length"))
            page.save()

        return response
