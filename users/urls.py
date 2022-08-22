"""poezdka URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views

urlpatterns = [
    path('registration', views.registration),
    path('auth', views.auth),
    path('delete_user', views.delete_user),
    path('', include('social_django.urls', namespace='social')),
    path('get_user', views.get_user),
    path('update_user', views.update_user),
    path('change_photo', views.change_photo),
    path('review<int:id_>', views.review),
    path('get_reviews', views.get_reviews),
    path('oauth_user', views.oauth_user),
    path('reset_password', views.reset_password),
    path('check_code', views.check_code),
    path('reset_password_confirm', views.reset_password_confirm),
    path('get_questions', views.get_questions),
    path('get_blog', views.get_blog),
]
