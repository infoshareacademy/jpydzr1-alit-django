from datetime import datetime, timedelta
from django.db.models import Value, CharField, Case, When, Q
from django.shortcuts import render

from .datagathering import NewDataFrame
from .models import *
from . import api



def siteSettings(request, what_type=None):
    set_date_top = "date_top"
    set_date_end = "date_end"
    set_continent = "continent"
    set_country = "country"
    data = "covid"


    # App memory status
    if request.POST:
        body = request.body.decode('utf-8')
        if len(body) > 0:
            if body[0:8] == set_date_top:
                request.session[set_date_top] = body[-10:]
            if body[0:8] == set_date_end:
                request.session[set_date_end] = body[-10:]
            if body[0:9] == set_continent:
                request.session[set_continent] = body[10:]
                request.session[set_country] = "0"
            if body[0:7] == set_country:
                print(body)
                request.session[set_country] = body[8:]
                request.session[set_continent] = "0"
    else:
        if not request.session.get("active", False):
            request.session["active"] = True
            request.session.set_expiry(3600)  # 60 minutes
            request.session[set_date_top] = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            request.session[set_date_end] = request.session[set_date_top]
            request.session[set_continent] = "0"
            request.session[set_country] = "0"

    # Continent list
    continents = Continent.objects.annotate(
        selected=Case(When(id=request.session[set_continent], then=Value("selected")),
                      default=Value(""), output_field=CharField())).all().order_by(set_continent)

    # Country list
    countries = Country.objects.annotate(
        selected=Case(When(id=request.session[set_country], then=Value("selected")),
                      default=Value(""), output_field=CharField())).all().order_by(set_country)

    # Covid19 one country
    if request.session[set_country] != "0" and request.session[set_continent] == "0":
        if what_type == 'dC':
            covid = CovidCalc.objects.values('date', 'country', 'dailyCases')\
                                            .filter(Q(country_id=request.session[set_country])
                                            & Q(date__gte=request.session[set_date_top])
                                            & Q(date__lte=request.session[set_date_end])).order_by('date')
        elif what_type == 'dR':
            covid = CovidCalc.objects.values('date', 'country', 'dailyRecovered')\
                                              .filter(Q(country_id=request.session[set_country])
                                              & Q(date__gte=request.session[set_date_top])
                                              & Q(date__lte=request.session[set_date_end]))\
                                              .order_by('date')
        elif what_type == 'dD':
            covid = CovidCalc.objects.values('date', 'country', 'dailyDeaths')\
                                              .filter(Q(country_id=request.session[set_country])
                                              & Q(date__gte=request.session[set_date_top])
                                              & Q(date__lte=request.session[set_date_end]))\
                                              .order_by('date')
        elif what_type == 'aC':
            covid = CovidCalc.objects.values('date', 'country', 'activeCases')\
                                              .filter(Q(country_id=request.session[set_country])
                                              & Q(date__gte=request.session[set_date_top])
                                              & Q(date__lte=request.session[set_date_end]))\
                                              .order_by('date')
        elif what_type == 'aCp100':
            covid = CovidCalc.objects.values('date', 'country', 'activeCasesPer100k')\
                                              .filter(Q(country_id=request.session[set_country])
                                              & Q(date__gte=request.session[set_date_top])
                                              & Q(date__lte=request.session[set_date_end]))\
                                              .order_by('date')
        elif what_type == 'dCS':
            covid = CovidCalc.objects.values('date', 'country', 'dailyCasesSmooth')\
                                              .filter(Q(country_id=request.session[set_country])
                                              & Q(date__gte=request.session[set_date_top])
                                              & Q(date__lte=request.session[set_date_end]))\
                                              .order_by('date')
        elif what_type == 'dRS':
            covid = CovidCalc.objects.values('date', 'country', 'dailyRecoveredSmooth')\
                                              .filter(Q(country_id=request.session[set_country])
                                              & Q(date__gte=request.session[set_date_top])
                                              & Q(date__lte=request.session[set_date_end]))\
                                              .order_by('date')
        elif what_type == 'dDS':
            covid = CovidCalc.objects.values('date', 'country', 'dailyDeathsSmooth')\
                                              .filter(Q(country_id=request.session[set_country])
                                              & Q(date__gte=request.session[set_date_top])
                                              & Q(date__lte=request.session[set_date_end]))\
                                              .order_by('date')
        elif what_type == 'cF':
            covid = CovidCalc.objects.values('date', 'country', 'caseFatality')\
                                              .filter(Q(country_id=request.session[set_country])
                                              & Q(date__gte=request.session[set_date_top])
                                              & Q(date__lte=request.session[set_date_end]))\
                                              .order_by('date')
        elif what_type == 'iR':
            covid = CovidCalc.objects.values('date', 'country', 'incidenceRate')\
                                              .filter(Q(country_id=request.session[set_country])
                                              & Q(date__gte=request.session[set_date_top])
                                              & Q(date__lte=request.session[set_date_end]))\
                                              .order_by('date')
        else:
            covid = CovidApi.objects.filter(Q(country_id=request.session[set_country])
                                        & Q(date__gte=request.session[set_date_top])
                                        & Q(date__lte=request.session[set_date_end])).order_by('date')

        #print(covid)


    # Covid one continent
    if request.session[set_continent] != "0" and request.session[set_country] == "0":
        covid = None

    # Covid all countries
    if request.session[set_continent] == "0" and request.session[set_country] == "0":
        covid = CovidApi.objects.filter(Q(date__gte=request.session[set_date_top])
                                      & Q(date__lte=request.session[set_date_end])).order_by('-date')

    return_data = {set_date_top: request.session[set_date_top], set_date_end: request.session[set_date_end],
                   set_continent: continents, set_country: countries, data: covid}
    #print(return_data.covid)

    return return_data


def index(request):
    data = siteSettings(request)
    return render(request, "index.html", data)


def login(request):
    data = siteSettings(request)
    return render(request, "login.html", data)


def dailyCases(request):
    case = 'dC'
    data = siteSettings(request, case)
    return render(request, "dailyCases.html", data)


def dailyRecovered(request):
    case = 'dR'
    data = siteSettings(request, case)
    return render(request, "dailyRecovered.html", data)


def dailyDeaths(request):
    case = 'dD'
    data = siteSettings(request, case)
    return render(request, "dailyDeaths.html", data)


def activeCases(request):
    case = 'aC'
    data = siteSettings(request, case)
    return render(request, "activeCases.html", data)


def activeCasesPer100k(request):
    case = 'aCp100'
    data = siteSettings(request, case)
    return render(request, "activeCasesPer100k.html", data)


def dailyCasesSmooth(request):
    case = 'dCS'
    data = siteSettings(request, case)
    return render(request, "dailyCasesSmooth.html", data)


def dailyRecoveredSmooth(request):
    case = 'dRS'
    data = siteSettings(request, case)
    return render(request, "dailyRecoveredSmooth.html", data)


def dailyDeathsSmooth(request):
    case = 'dDS'
    data = siteSettings(request, case)
    return render(request, "dailyDeathsSmooth.html", data)


def mortality(request):
    case = 'm'
    data = siteSettings(request, case)
    return render(request, "mortality.html", data)


def caseFatality(request):
    case = 'cF'
    data = siteSettings(request, case)
    return render(request, "caseFatality.html", data)


def incidenceRate(request):
    case = 'iR'
    data = siteSettings(request, case)
    return render(request, "incidenceRate.html", data)


def loadData(request):
    data = siteSettings(request)
    #app = api.CovidToDb()
    #app.runApiToDb()
    #baza = NewDataFrame()
    #baza.writetodb()
    return render(request, "index.html", data)

# def examplePlot():
#     x = np.linspace(0, 12.56, 41)
#     y = np.sin(x)
#     y2 = np.sin(1.2 * x)
#     data = [
#         go.Scatter(
#             name='Sin(x)',
#             x=x,
#             y=y,
#         ),
#         go.Scatter(
#             name='Sin(1.2x)',
#             x=x,
#             y=y2,
#         ),
#     ]
#     layout = go.Layout(
#         xaxis=dict(
#             title='x'
#         ),
#         yaxis=dict(
#             title='Value',
#             hoverformat='.2f'
#         ),
#     )
#     fig = go.Figure(data=data, layout=layout)
#     plot_div = py.plot(fig, include_plotlyjs=False, output_type='div')
#     return plot_div
