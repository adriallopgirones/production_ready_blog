"""
ASGI config for production_ready_blog_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

import core_apps.chat.routing

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "production_ready_blog_project.settings"
)

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(core_apps.chat.routing.websocket_urlpatterns))
        ),
    }
)
