from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.shortcuts import render
from django.views.decorators.cache import cache_page

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
# Create your views here.

#@cache_page(CACHE_TTL)
def home(requests):
    return render(requests, 'home/welcome.html')

@cache_page(CACHE_TTL)
def cases(requests):
    return render(requests, 'home/cases.html')

#@cache_page(CACHE_TTL)
def deaths(requests):
    return render(requests, 'home/deaths.html')

#@cache_page(CACHE_TTL)
def mortality(requests):
    return render(requests, 'home/mortality.html')

#@cache_page(CACHE_TTL)
def emortality(requests):
    return render(requests, 'home/emortality.html')

#@cache_page(CACHE_TTL)
def recovered(requests):
    return render(requests, 'home/recovered.html')

#@cache_page(CACHE_TTL)
def vaccinations(requests):
    return render(requests, 'home/vaccinations.html')

@cache_page(CACHE_TTL)
def login(requests):
    return render(requests, 'home/login.html')