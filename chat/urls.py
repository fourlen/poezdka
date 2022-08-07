from django.urls import re_path
from django.urls import path
import chat.views as views

from . import consumers

urlpatterns = [
    path('get_chat', views.get_chat)
]