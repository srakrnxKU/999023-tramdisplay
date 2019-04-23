from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("tram/<id>", views.get_tram, name="tram"),
    path("tram/<id>/set/time/<int:time>", views.set_tram_time, name="set_tram_time"),
    path("tram/<id>/set/seats/<int:seats>", views.set_tram_seats, name="set_tram_seat"),
]

