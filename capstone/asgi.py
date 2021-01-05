"""
ASGI config for capstone project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from classroom.consumers import ChatConsumer, UserConsumer


application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": (URLRouter([
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()), 
    re_path(r'', UserConsumer.as_asgi()),
  ]))

})