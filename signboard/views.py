from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Min
from .models import Tram, Line
from django.core import serializers
from time import localtime, gmtime, strftime

# Create your views here.


def index(request):
    lines = Line.objects.all()
    trams = {
        l: Tram.objects.filter(line=l, mins_left__lte=15).order_by("mins_left")[:3]
        for l in lines
    }
    print(trams)
    return render(
        request,
        "signboard.html",
        {"trams": trams, "time": strftime("%H:%M", localtime())},
    )
    # return HttpResponse("Hello!")


def get_tram(request, id):
    tram = Tram.objects.get(pk=id)
    return JsonResponse(
        {
            "id": tram.id,
            "name": tram.name,
            "seats": {"full": tram.full_seats, "remaining": tram.remaining_seats},
            "line": {"number": tram.line.line_number},
        }
    )


def set_tram_time(request, id, time):
    tram = Tram.objects.get(pk=id)
    tram.mins_left = time
    tram.save()
    return HttpResponse("done")


def set_tram_seats(request, id, seats):
    tram = Tram.objects.get(pk=id)
    tram.remaining_seats = seats
    tram.save()
    return HttpResponse("done")
