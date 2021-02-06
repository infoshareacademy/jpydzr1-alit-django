from django.contrib import admin

# Register your models here.
from .models import Continent, Country, CovidApi, CovidCalc

@admin.register(Continent)
class AdminContinent(admin.ModelAdmin):
    fields = ('continent',)


@admin.register(Country)
class AdminCountry(admin.ModelAdmin):
    fields = ('country', 'iso2', 'population', 'continent')


@admin.register(CovidApi)
class AdminCovidApi(admin.ModelAdmin):
    fields = ('date', 'country', 'confirmed', 'deaths', 'recovered', 'active')


@admin.register(CovidCalc)
class AdminCovidCalc(admin.ModelAdmin):
    fields = ('date', 'country', 'dailyCases', 'dailyRecovered', 'dailyDeaths', 'activeCases')



