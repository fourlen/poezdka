from django.urls import re_path

from . import consumers

cc = consumers.ChatConsumer()

websocket_urlpatterns = [
    re_path(r'ws/', cc.as_asgi())
]