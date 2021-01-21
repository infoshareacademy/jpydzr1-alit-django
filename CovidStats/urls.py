from django.conf.urls import url
from django.urls import path
from . import views
from CovidStats.views import IndexView, MyView
from CovidStats.dash_apps.finished_apps import simpleexample


url(r'^view_project/(?P<project_id>\d+)/$', views.IndexView.as_view, name='View_stats'),
urlpatterns = [
    path('', views.home, name='home'),
    path('cases/', views.cases, name='cases'),
    path('deaths/', IndexView.as_view(template_name='home/deaths.html')),
    path('<str:country>/info/', IndexView.as_view(template_name='home/deaths.html')),
    path('<str:country>/mortality/', IndexView.as_view(template_name='home/mortality.html')),
    path('<str:country>/deaths/', IndexView.as_view(template_name='home/deaths.html')),
    path('emortality/', views.emortality, name='emortality'),
    path('recovered/', views.recovered, name='recovered'),
    path('vaccinations/', views.vaccinations, name='vaccinations'),
    path('login/', views.login, name='login'),
]