from django.contrib import admin
from .models import Line, Tram, SignAlert, Stop

# Register your models here.
admin.site.register(Line)
admin.site.register(Tram)
admin.site.register(SignAlert)
admin.site.register(Stop)
