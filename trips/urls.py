from django.urls import path

from trips import views

urlpatterns = [
    path('add_trip', views.add_trip),
]
