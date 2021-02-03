from django.db import models


class Country(models.Model):
    Country = models.CharField(max_length=100)
    ISO3 = models.CharField(max_length=3, unique=True)
    ISO2 = models.CharField(max_length=2)
    population = models.IntegerField(default=0)

    class Meta:
        ordering = ['Country']

    def __str__(self):
        return self.country


class CovidDataSet(models.Model):
    Date = models.DateField(max_length=10)
    Country = models.CharField(max_length=100)
    Confirmed = models.IntegerField(default=0)
    Recovered = models.IntegerField(default=0)
    Deaths = models.IntegerField(default=0)
    iso2 = models.CharField(max_length=2)
    iso3 = models.CharField(max_length=3)
    Population = models.IntegerField(default=0)
    Daily_tests = models.IntegerField(default=0)
    Daily_recovered = models.IntegerField(default=0)
    Daily_deaths = models.IntegerField(default=0)
    Daily_cases = models.IntegerField(default=0)
    Active_cases = models.IntegerField(default=0)
    Active_per_100k = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    Daily_cases_smooth = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    Daily_deaths_smooth = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    Positive_test_rate = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    Tests_per_case = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    Case_fatality = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    Incidence_rate = models.DecimalField(max_digits=10, decimal_places=4, default=0)

class Mortality(models.Model):
    location = models.CharField(max_length=100)
    date = models.CharField(max_length=10)
    p_scores_all_ages = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    p_scores_15_64 = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    p_scores_65_74 = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    p_scores_75_84 = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    p_scores_85plus = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    deaths_2020_all_ages = models.IntegerField(default=0)
    average_deaths_2015_2019_all_ages = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    deaths_2015_all_ages = models.IntegerField(default=0)
    deaths_2016_all_ages = models.IntegerField(default=0)
    deaths_2017_all_ages = models.IntegerField(default=0)
    deaths_2018_all_ages = models.IntegerField(default=0)
    deaths_2019_all_ages = models.IntegerField(default=0)
    deaths_2010_all_ages = models.IntegerField(default=0)
    deaths_2011_all_ages = models.IntegerField(default=0)
    deaths_2012_all_ages = models.IntegerField(default=0)
    deaths_2013_all_ages = models.IntegerField(default=0)
    deaths_2014_all_ages = models.IntegerField(default=0)
    Week = models.IntegerField(default=0)
    deaths_2021_all_ages = models.IntegerField(default=0)

