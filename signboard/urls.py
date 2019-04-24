from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("tram/<id>", views.get_tram, name="tram"),
    path("tram/<id>/set/time/<int:time>", views.set_tram_time, name="set_tram_time"),
    path("tram/<id>/set/seats/<int:seats>", views.set_tram_seats, name="set_tram_seat"),
    path(
        "line/<id>/set/congestion/<int:congestion>",
        views.set_line_congestion,
        name="set_line_congestion",
    ),
    path("alert/new/<text>", views.new_alert, name="new_alert"),
    path("alert/hide", views.hide_alert, name="hide_alert"),
    path("routemap/", views.routemap, name="routemap"),
    path(
        "stop/<id>/set/waiting/<int:waiting>",
        views.set_stop_waiting,
        name="set_stop_waiting",
    ),
]

