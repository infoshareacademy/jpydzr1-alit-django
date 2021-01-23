from django.db import models


class Continent(models.Model):
    continent = models.CharField(max_length=50)

    def __str__(self):
        return self.continent


class Country(models.Model):
    country = models.CharField(max_length=100)
    iso2 = models.CharField(max_length=2)
    population = models.IntegerField(default=0)
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.country} - {self.continent}"


class CovidApi(models.Model):
    date = models.CharField(max_length=10)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    confirmed = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    recovered = models.IntegerField(default=0)
    active = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.date} - {self.country}"


class CovidCalc(models.Model):
    date = models.CharField(max_length=10)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    dailyCases = models.IntegerField(default=0)
    dailyRecovered = models.IntegerField(default=0)
    dailyDeaths = models.IntegerField(default=0)
    activeCases = models.IntegerField(default=0)
    activeCasesPer100k = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    dailyCasesSmooth = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    dailyRecoveredSmooth = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    dailyDeathsSmooth = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    mortality = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    caseFatality = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    incidenceRate = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.date} - {self.country}"
