from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Min
from .models import Tram, Line
from django.core import serializers

# Create your views here.


def index(request):
    lines = Line.objects.all()
    trams = {l: Tram.objects.filter(line=l).order_by("mins_left")[:3] for l in lines}
    print(trams)
    return render(request, "signboard.html", {"trams": trams})
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
