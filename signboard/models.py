from django.db import models

# Create your models here.


class Line(models.Model):
    line_number = models.CharField(max_length=10, primary_key=True)
    line_color = models.CharField(max_length=24)
    line_text_color = models.CharField(max_length=24)
    delay = models.BooleanField(default=False)

    def __str__(self):
        return "รถโดยสารสาย {}".format(self.line_number)


class Tram(models.Model):
    name = models.CharField(max_length=20)
    line = models.ForeignKey(Line, on_delete=models.CASCADE, null=True)
    full_seats = models.IntegerField()
    occupied_seats = models.IntegerField()
    mins_left = models.IntegerField()

    def __str__(self):
        return "รถโดยสารรหัส {}".format(self.name)
    
    @property
    def remaining_seats(self):
        return self.full_seats - self.occupied_seats


class SignAlert(models.Model):
    text = models.CharField(max_length=140)
    shown = models.BooleanField(default=True)

    def __str__(self):
        return self.text
