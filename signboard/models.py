from django.db import models

# Create your models here.


class Line(models.Model):
    line_number = models.CharField(primary_key=True)

    def __str__(self):
        return "รถโดยสารสาย {}".format(self.line_number)


class Tram(models.Model):
    name = models.CharField()
    line = models.ForeignKey(Line, on_delete=models.CASCADE)
    full_seats = models.IntegerField()
    remaining_seats = models.IntegerField()
