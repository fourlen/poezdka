<<<<<<< HEAD
from django.urls import path

from cars import views

urlpatterns = [
    path('add', views.add_car),
    path('delete<id:int>', views.delete_car)
]
=======
from django.urls import path

from cars import views

urlpatterns = [
    path('add', views.add_car),
    path('delete<int:id>', views.delete_car)
]
>>>>>>> 5ecbd230b4714f4332482e058639a3fcc17c7079
