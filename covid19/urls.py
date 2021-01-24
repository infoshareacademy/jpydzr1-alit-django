from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("login/", views.login),
    path("settings/", views.index),
    path("dailyCases/", views.dailyCases),
    path("dailyRecovered/", views.dailyRecovered),
    path("dailyDeaths/", views.dailyDeaths),
    path("activeCases/", views.activeCases),
    path("activeCasesPer100k/", views.activeCasesPer100k),
    path("dailyCasesSmooth/", views.dailyCasesSmooth),
    path("dailyRecoveredSmooth/", views.dailyRecoveredSmooth),
    path("dailyDeathsSmooth/", views.dailyDeathsSmooth),
    path("mortality/", views.mortality),
    path("caseFatality/", views.caseFatality),
    path("incidenceRate/", views.incidenceRate),
    path("loadData/", views.loadData),
]
