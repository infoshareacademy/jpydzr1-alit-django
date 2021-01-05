from django.urls import path
from . import views
from CovidStats.dash_apps.finished_apps import simpleexample

urlpatterns = [
    path('', views.home, name='home'),
    path('buttons/', views.buttons, name='buttons')
]