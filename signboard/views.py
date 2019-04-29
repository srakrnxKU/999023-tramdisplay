from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Min
from .models import Tram, Line, SignAlert, Stop
from django.core import serializers
from time import localtime, gmtime, strftime
import json

# Create your views here.


def index(request):
    lines = Line.objects.order_by("line_number")
    trams = {
        l: Tram.objects.filter(line=l, mins_left__lte=15).order_by("mins_left")[:2]
        for l in lines
    }
    alert = SignAlert.objects.order_by("-pk")[0]
    print(trams)
    return render(
        request,
        "signboard.html",
        {"trams": trams, "alert": alert, "time": strftime("%H:%M", localtime())},
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
    tram.occupied_seats = seats
    tram.save()
    return HttpResponse("done")


def set_line_congestion(request, id, congestion):
    line = Line.objects.get(pk=id)
    line.delay = bool(congestion)
    line.save()
    return HttpResponse("done")


def new_alert(request, text):
    alert = SignAlert()
    alert.text = text
    alert.save()
    return HttpResponse("done")


def hide_alert(request):
    alert = SignAlert.objects.order_by("-pk")[0]
    alert.shown = False
    alert.save()
    return HttpResponse("done")


def routemap(request):
    return render(request, "routemap.html")


def routemap_divs(request):
    stops = Stop.objects.all()
    return render(request, "routemap_divs.html", {"stops": stops})


def set_stop_waiting(request, id, waiting):
    stop = Stop.objects.get(pk=id)
    stop.waiting = waiting
    stop.save()
    return HttpResponse("{}: {}".format(stop.name, stop.waiting))


@csrf_exempt
def assistant(request):
    if request.method == "POST":
        data = json.loads(request.body)
        intent = data["queryResult"]["intent"]["displayName"]
        if intent == "Arrival time":
            tram = Tram.objects.order_by("mins_left")[0]
            text = "The nearest bus is for line {}, and will arrive in {} minutes.".format(
                tram.line.line_number, tram.mins_left
            )
            print(text)
        elif intent == "Specified line":
            line_number = int(data["queryResult"]["parameters"]["lineNumber"])
            trams = Tram.objects.filter(line=line_number, mins_left__lte=15).order_by(
                "mins_left"
            )
            if trams.count() == 0:
                text = "No bus for line number {} will arrive in 15 minutes.".format(
                    line_number
                )
            else:
                tram = trams[0]
                text = "Bus line {} will arrive in {} minutes.".format(
                    tram.line.line_number, tram.mins_left
                )
        else:
            text = "Sorry, I don't understand."
    else:
        text = "Sorry, I don't understand."
    json_structure = {
        "fulfillmentText": text,
        "payload": {
            "google": {
                "richResponse": {"items": [{"simpleResponse": {"textToSpeech": text}}]}
            }
        },
    }
    return JsonResponse(json_structure)
