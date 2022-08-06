from django.urls import path

from booking import views

urlpatterns = [
    path('book<int:id_>/<int:seat>', views.book),
    path('cancel<int:id_>', views.cancel_booking),
]
