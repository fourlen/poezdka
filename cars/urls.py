from django.urls import path

from cars import views

urlpatterns = [
    path('add', views.add_car),
    path('delete<int:id>', views.delete_car),
    path('get_cars', views.get_cars),
]
