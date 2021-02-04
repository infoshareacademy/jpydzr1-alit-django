from django.shortcuts import render
from .models import *

# Create your views here.



def home(requests):
    return render(requests, 'Covid/welcome.html')
