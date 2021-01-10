from django.urls import path
from . import views
from CovidStats.dash_apps.finished_apps import simpleexample

urlpatterns = [
    path('', views.home, name='home'),
    path('cases/', views.cases, name='cases'),
    path('deaths/', views.deaths, name='deaths'),
    path('mortality/', views.mortality, name='mortality'),
    path('emortality/', views.emortality, name='emortality'),
    path('recovered/', views.recovered, name='recovered'),
    path('vaccinations/', views.vaccinations, name='vaccinations'),
    path('login/', views.login, name='login')
]