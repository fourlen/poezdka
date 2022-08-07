from django.urls import re_path
from django.urls import path
import views

from . import consumers

websocket_urlpatterns = [
    re_path(r'/ws/chat/', consumers.ChatConsumer),
    path('get_chat', views.get_chat)
]