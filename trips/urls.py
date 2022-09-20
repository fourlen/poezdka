from django.urls import path

from trips import views

urlpatterns = [
    path('add_trip', views.add_trip),
    path('delete<int:id_>', views.delete_trip),
    path('get_trips', views.get_trips),
    path('get_booked_trips', views.get_booked_trips),
    path('get_past_trips', views.get_past_trips),
    path('get_past_booked_trips', views.get_past_booked_trips),
    path('get_all_trips', views.main_trips),
    path('get_all_drivers_trips', views.main_drivers_trips),
    path('rank', views.get_lvl),

]
