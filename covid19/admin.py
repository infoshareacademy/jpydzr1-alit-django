from django.contrib import admin

# Register your models here.
from .models import Continent, Country, CovidApi, CovidCalc

admin.site.register(Continent)
admin.site.register(Country)
admin.site.register(CovidApi)
admin.site.register(CovidCalc)
