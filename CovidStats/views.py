from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt

# Create your views here.

def home(requests):
    return render(requests, 'home/welcome.html')

@xframe_options_exempt
def buttons(requests):
    return render(requests, 'home/buttons.html')