from django.urls import re_path
from .consumer import QWANConsumer

websocket_urlpatterns = [
    re_path(r'ws/qwan/$', QWANConsumer.as_asgi()),
]
