import datetime
import json
import time
import requests
from django.db import connection
from covid19.models import CovidApi, Country


class CovidToDb():
    def __init__(self):
        self.api = "https://api.covid19api.com"
        self.dateTop = None
        self.dateEnd = None
        self.progress = 0
        self.scope = 5
        self.timeout = 2
        self.listCountries = self.listCountries()
        return

    def getProgress(self):
        return self.progress

    def runApiToDb(self):
        self.progress = 0
        if len(self.listCountries) > 0:
            with connection.cursor() as cursor:
                qs = CovidApi.objects.order_by("-date")[:1]
                print(qs)
                print(len(qs))
                if len(qs) > 0:
                    self.dateTop = qs[0].date
                    print(self.dateTop)
                else:
                    self.dateTop = "2020-01-22"
                #self.dateEnd = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y=%m-%d")
                self.dateEnd = '2021-02-05'
                if self.dateTop > self.dateEnd:
                    self.dateTop = self.dateEnd
                countries = Country.objects.all().order_by("country")
                lastRecord = len(countries)
                recno = 0
                for item in countries:
                    print(item)
                    value = self.countryValue(item.country.lower().replace(" ", "-"))
                    print(value)
                    if len(value) > 0:
                        cursor.execute(f"DELETE FROM covid19_covidapi WHERE country_id = {item.id} "
                                       f"and date >= '{self.dateTop}' and date <= '{self.dateEnd}'")
                        for item2 in value:
                            sql = f"INSERT INTO covid19_covidapi (date,country_id,confirmed,deaths,recovered,active) " \
                                  f"VALUES ('{item2}',{item.id}," \
                                f"{value[item2][0]},{value[item2][1]},{value[item2][2]},{value[item2][3]})"
                            cursor.execute(sql)
                    recno = recno + 1
                    self.progress = int(round(recno / lastRecord * 100, 0))
        self.progress = 100
        return

    def listCountries(self):
        value = []
        link = f"{self.api}/countries"
        try:
            for i in range(self.scope):
                rqs = requests.get(link)
                if rqs.status_code == 200:
                    data = json.loads(rqs.text)
                    for item in data:
                        value.append(item["Slug"])
                    break
                else:
                    time.sleep(self.timeout)
        except ValueError:
            value = []
        return value

    def countryValue(self, country):
        value = {}
        link = f"{self.api}/country/{country}?from={self.dateTop}T00:00:00Z&to={self.dateEnd}T23:59:59Z"
        modes = ["Confirmed", "Deaths", "Recovered", "Active"]
        if country in self.listCountries:
            try:
                for i in range(self.scope):
                    rqs = requests.get(link)
                    if rqs.status_code == 200:
                        data = json.loads(rqs.text)
                        for day in data:
                            temp = []
                            for mode in modes:
                                temp.append(day[mode])
                            value[day["Date"][:10]] = temp
                        break
                    else:
                        time.sleep(self.timeout)
            except ValueError:
                value = {}
        return value
