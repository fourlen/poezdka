from django.urls import re_path
from django.urls import path
import views
from . import consumers

cc = consumers.ChatConsumer()

websocket_urlpatterns = [
    re_path(r'ws/', cc.as_asgi()),
    path('get_chat', views.get_chat)
]