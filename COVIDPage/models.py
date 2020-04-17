from django.db import models
import datetime


class CovidData(models.Model):
    date = models.DateField(primary_key=True)
    state = models.CharField(max_length=50)
    total_cases = models.IntegerField()
    new_case = models.IntegerField()
    total_deaths = models.IntegerField()
    new_deaths = models.IntegerField()
    active_case = models.IntegerField()
