from django.contrib import admin
from .models import Line, Tram, SignAlert

# Register your models here.
admin.site.register(Line)
admin.site.register(Tram)
admin.site.register(SignAlert)
