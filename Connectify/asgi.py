"""
ASGI config for Connectify project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# imported
from channels.routing import ProtocolTypeRouter,URLRouter
from django.core.asgi import get_asgi_application
from ChatApp import routing

#imported for one to one
from django.urls import path
from channels.auth import AuthMiddlewareStack
# from ChatApp.consumers import PersonalChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Connectify.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket":AuthMiddlewareStack(
         URLRouter(
            routing.websocket_urlpatterns
        )
    )
})

# one to one

# application = get_asgi_application()

# application = ProtocolTypeRouter({
#     'websocket':AuthMiddlewareStack(
#         URLRouter({
#             path('ws/<int:id>',PersonalChatConsumer)
#         })
#     )
# })