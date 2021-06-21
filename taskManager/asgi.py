"""
ASGI config for taskManager project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
# from .channelsmiddleware import JwtAuthMiddlewareStack


import websocket.routing 

os.environ.setdefault('DJANGO_SETT INGS_MODULE', 'taskManager.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket":
    # AuthMiddlewareStack(
    # AllowedHostsOriginValidator(
        # JwtAuthMiddlewareStack(
            URLRouter(
                websocket.routing.websocket_urlpatterns
            )
        # )
    # )
})

