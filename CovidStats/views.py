from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.http import request
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView, ListView
import numpy as np
import plotly.offline as py
import plotly.graph_objs as go

from CovidStats.dash_apps.finished_apps.newdataframe import NewDataFrame, SummaryDF, ExcessMort, VacDataFrame, \
    CountryList

completeSet = NewDataFrame().return_df()
sumCases = SummaryDF().return_sumdf()
excessMortSet = ExcessMort().return_mortdf()
vaccSet = VacDataFrame().return_vacdf()
listOfCountries = CountryList().return_coutrylist()

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


# Create your views here.

class MyView(ListView):
    template_name = 'home/deaths.html'


class IndexView(TemplateView):
    template_name = 'home/deaths.html'
    variable = 'Poland'

    def get_request(self, request):
        self.variable = self.request.POST.get('country')
        print(self.variable)

    def get_context_data(self, **kwargs):
        self.variable = self.request.POST.get('country', '')
        print(self.variable)
        context = super().get_context_data(**kwargs)
        context['plot'] = examplePlot()
        context['card1'] = cardValue()
        return context


def cardValue():
    filtered_df = sumCases[sumCases.Country == 'Poland']
    # sumCases[sumCases.Country == 'Poland']['Deaths'].to_string(index=False)
    val = filtered_df['Deaths'].to_string(index=False)
    print(val)
    return val


def examplePlot():
    x = np.linspace(0, 12.56, 41)
    y = np.sin(x)
    y2 = np.sin(1.2 * x)

    data = [
        go.Scatter(
            name='Sin(x)',
            x=x,
            y=y,
        ),

        go.Scatter(
            name='Sin(1.2x)',
            x=x,
            y=y2,
        ),
    ]

    layout = go.Layout(
        xaxis=dict(
            title='x'
        ),

        yaxis=dict(
            title='Value',
            hoverformat='.2f'
        ),
    )

    fig = go.Figure(data=data, layout=layout)
    plot_div = py.plot(fig, include_plotlyjs=False, output_type='div')
    return plot_div


# @cache_page(CACHE_TTL)
def home(requests):
    return render(requests, 'home/welcome.html')


@cache_page(CACHE_TTL)
def cases(requests):
    return render(requests, 'home/cases.html')


# @cache_page(CACHE_TTL)
# def deaths(requests):
#    return render(requests, 'home/deaths.html')

# @cache_page(CACHE_TTL)
# def mortality(requests):
#    return render(requests, 'home/mortality.html')

# @cache_page(CACHE_TTL)
def emortality(requests):
    return render(requests, 'home/emortality.html')


# @cache_page(CACHE_TTL)
def recovered(requests):
    return render(requests, 'home/recovered.html')


# @cache_page(CACHE_TTL)
def vaccinations(requests):
    return render(requests, 'home/vaccinations.html')


@cache_page(CACHE_TTL)
def login(requests):
    return render(requests, 'home/login.html')
