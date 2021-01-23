from datetime import datetime, timedelta
from django.db.models import Value, CharField, Case, When
from django.shortcuts import render
from .models import *
from .api import covidToDb


def settings(request):
    key1 = "date_top"
    key2 = "date_end"
    key3 = "continent"
    key4 = "country"
    key5 = "range"
    key6 = "covid"

    if request.POST:
        body = request.body.decode('utf-8')
        if len(body) > 0:
            if body[0:8] == key1:
                request.session[key1] = body[-10:]
            if body[0:8] == key2:
                request.session[key2] = body[-10:]
            if body[0:9] == key3:
                request.session[key3] = body[10:]
                request.session[key4] = "0"
            if body[0:7] == key4:
                request.session[key4] = body[8:]
                request.session[key3] = "0"
    else:
        if not request.session.get("active", False):
            request.session["active"] = True
            request.session.set_expiry(3600)  # 60 minutes
            request.session[key1] = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            request.session[key2] = request.session[key1]
            request.session[key3] = "0"
            request.session[key4] = "0"

    continents = Continent.objects.annotate(
        selected=Case(When(id=request.session[key3], then=Value("selected")),
                      default=Value(""), output_field=CharField())).all().order_by(key3)
    countries = Country.objects.annotate(
        selected=Case(When(id=request.session[key4], then=Value("selected")),
                      default=Value(""), output_field=CharField())).all().order_by(key4)
    covid = CovidApi.objects.all()

    r_user = [request.session[key1], request.session[key2], request.session[key3], request.session[key4]]

    x = {key1: request.session[key1], key2: request.session[key2], key3: continents,
         key4: countries, key5: r_user, key6: covid}
    return x


def index(request):
    x = settings(request)
    return render(request, "index.html", x)


def login(request):
    x = settings(request)

    # Example, the login panel is available only when "Wszystkie kontynenty" and "Wszystkie kraje" is selected,
    # 0 - date top,
    # 1 - date end,
    # 2 - id continent ("0" - not selected, all continents),
    # 3 - id country ("0" - not selected, all countries).
    if x["range"][2] != "0" or x["range"][3] != "0":
        return render(request, "index.html", x)
    return render(request, "login.html", x)


def dailyCases(request):
    x = settings(request)
    return render(request, "dailyCases.html", x)


def dailyRecovered(request):
    x = settings(request)
    return render(request, "dailyRecovered.html", x)


def dailyDeaths(request):
    x = settings(request)
    return render(request, "dailyDeaths.html", x)


def activeCases(request):
    x = settings(request)
    return render(request, "activeCases.html", x)


def activeCasesPer100k(request):
    x = settings(request)
    return render(request, "activeCasesPer100k.html", x)


def dailyCasesSmooth(request):
    x = settings(request)
    return render(request, "dailyCasesSmooth.html", x)


def dailyRecoveredSmooth(request):
    x = settings(request)
    return render(request, "dailyRecoveredSmooth.html", x)


def dailyDeathsSmooth(request):
    x = settings(request)
    return render(request, "dailyDeathsSmooth.html", x)


def mortality(request):
    x = settings(request)
    return render(request, "mortality.html", x)


def caseFatality(request):
    x = settings(request)
    return render(request, "caseFatality.html", x)


def incidenceRate(request):
    x = settings(request)
    return render(request, "incidenceRate.html", x)


def loadData(request):
    x = settings(request)
    return render(request, "loadData.html", x)
