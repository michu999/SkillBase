from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings


class SlackLoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [
            '/accounts/slack/login/',
            '/accounts/slack/login/callback/',
            '/admin/',
            '/',  # Landing page
        ]

    def __call__(self, request):
        if not request.user.is_authenticated:
            path = request.path_info
            if not any(path.startswith(url) for url in self.exempt_urls):
                return redirect('landing')
        return self.get_response(request)