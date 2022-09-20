from django.urls import path

from booking import views

urlpatterns = [
    path('book<int:id_>', views.book),
    path('cancel<int:id_>', views.cancel_booking),
    path('driver_cancel', views.cancel_booking_for_driver),
]
