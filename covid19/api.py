import datetime
import json
import time
import requests
from django.db import connection


def covidToDb():
    pass

    # country = "POLAND"
    # c_id = 149
    # value = countryValue(country, "2021-01-01", "2021-01-14")
    # with connection.cursor() as cursor:
    #     cursor.execute(f"DELETE FROM covid19_covidapi WHERE country_id = {c_id}")
    #     for item in value:
    #         sql = f"INSERT INTO covid19_covidapi (date,country_id,confirmed,deaths,recovered,active) VALUES " \
    #               f"('{item}',{c_id},{value[item][0]},{value[item][1]},{value[item][2]},{value[item][3]})"
    #         cursor.execute(sql)
    # return


def countryValue(country, dateTop, dateEnd):
    api = "https://api.covid19api.com"
    value = {}
    modes = ["Confirmed", "Deaths", "Recovered", "Active"]
    link = api + "/country/" + country + "?from=" + dateTop + "T00:00:00Z&to=" + dateEnd + "T23:59:59Z"
    scope = 5
    timeout = 5
    try:
        for i in range(scope):
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
                time.sleep(timeout)
    except ValueError:
        value = {}
    return value
