from django.db import models


class CovidApi(models.Model):
    iso2 = models.CharField(max_length=2)