from django.db import models


class Country(models.Model):
    full_name = models.CharField(max_length=50)


class Report(models.Model):
    # TRANSMISSION_TYPES = (
    #     (,),
    # )
    # input_formats=['%d-%m-%Y']
    date = models.DateField()
    # country = models.ForeignKey(Country, on_delete=models.CASCADE)
    country = models.CharField(max_length=50)
    cases_total = models.IntegerField()
    cases_new = models.IntegerField()
    deaths_total = models.IntegerField()
    deaths_new = models.IntegerField()
    transmission_type = models.CharField(max_length=50)
    days_last_case = models.IntegerField()