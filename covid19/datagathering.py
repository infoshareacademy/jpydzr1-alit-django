import pandas as pd
from django_pandas.io import read_frame
from .models import Country, CovidCalc, CovidApi
from decimal import Decimal, DecimalException


pd.set_option('use_inf_as_na', True)


class NewDataFrame:
    def __init__(self):
        self.last_date = '2020-01-22'
        self.dfComplete = 0

    def calculate_data(self):
        self.qs = CovidApi.objects.select_related('country').filter(date__gt=self.last_date)
        population = []
        for q in self.qs:
            population.append(q.country.population)
        df2 = pd.DataFrame(population)
        df1 = read_frame(self.qs)
        self.dfComplete = pd.concat([df1, df2], axis=1)
        self.dfComplete.drop_duplicates(['date', 'country'])
        self.dfComplete = self.dfComplete.rename(columns={0: 'population'})
        self.dfComplete.sort_values(by=['date'])
        self.dfComplete['Daily_cases'] = self.dfComplete.groupby(['country'], group_keys=False)[
            "confirmed"].diff().fillna(0)
        self.dfComplete['Daily_recovered'] = self.dfComplete.groupby(['country'], group_keys=False)[
            "recovered"].diff().fillna(0)
        self.dfComplete['Daily_deaths'] = self.dfComplete.groupby(['country'], group_keys=False)[
            "deaths"].diff().fillna(0)
        self.dfComplete['Active_cases'] = self.dfComplete['confirmed'] - (
                self.dfComplete['recovered'] + self.dfComplete['deaths'])
        self.dfComplete['Active_per_100k'] = round(
            (self.dfComplete['Active_cases'] / self.dfComplete['population']) * 100000, 2).fillna(0)
        self.dfComplete['Daily_cases_smooth'] = round(
            self.dfComplete.groupby(['country'], group_keys=False)["Daily_cases"].rolling(window=7).mean().reset_index(
                0, drop=True), 2).fillna(0)
        self.dfComplete['Daily_deaths_smooth'] = round(
            self.dfComplete.groupby(['country'], group_keys=False)["Daily_deaths"].rolling(window=7).mean().reset_index(
                0, drop=True), 2).fillna(0)
        self.dfComplete['Case_fatality'] = round(self.dfComplete['deaths'] / self.dfComplete['confirmed'], 2).fillna(0)
        self.dfComplete['Incidence_rate'] = round(self.dfComplete['confirmed'] / self.dfComplete['population'],
                                                  2).fillna(0)
        self.dfComplete['Daily_cases'] = self.dfComplete['Daily_cases'].astype('int32')
        self.dfComplete['Daily_recovered'] = self.dfComplete['Daily_recovered'].astype('int32')
        self.dfComplete['Daily_deaths'] = self.dfComplete['Daily_deaths'].astype('int32')
        columns = ['id', 'confirmed', 'deaths', 'recovered', 'active', 'population']
        self.dfComplete = self.dfComplete.drop(columns, axis=1)

    def writetodb(self):
        qs = Country.objects.all()
        for dfrow in self.dfComplete.itertuples():
            try:
                #print(dfrow)
                dfrow = CovidCalc.objects.create(
                    date=dfrow.date,
                    country=qs.get(country=dfrow.country),
                    #country=dfrow.country,
                    dailyCases=dfrow.Daily_cases,
                    dailyRecovered=dfrow.Daily_recovered,
                    dailyDeaths=dfrow.Daily_deaths,
                    activeCases=dfrow.Active_cases,
                    activeCasesPer100k=dfrow.Active_per_100k,
                    dailyCasesSmooth=dfrow.Daily_cases_smooth,
                    dailyDeathsSmooth=dfrow.Daily_deaths_smooth,
                    caseFatality=dfrow.Case_fatality,
                    incidenceRate=dfrow.Incidence_rate
                )
            except (ValueError, DecimalException):
                print(dfrow)
                break

    def createCountryList(self):
        if Country.objects.count() == 0:
            for countryrow in self.dfRef.itertuples():
                countryrow = Country.objects.create(
                    Country=countryrow.Country,
                    ISO3=countryrow.iso3,
                    ISO2=countryrow.iso2,
                    population=countryrow.Population
                )

    def return_df(self):
        return self.dfComplete

    def df_info(self):
        return self.dfComplete.info(verbose=True)

    def set_last_date(self, date):
        self.last_date = date



# class ExcessMort:
#     def __init__(self):
#         self.urlMort = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/excess_mortality/excess_mortality.csv"
#         self.fileMort = pd.read_csv(self.urlMort)
#         self.dfMort = pd.DataFrame(self.fileMort)
#         self.dfMort = self.dfMort.fillna(0)
#
#     def writetodb(self):
#         Mortality.objects.all().delete()
#         for countryrow in self.dfMort.itertuples():
#             countryrow = Mortality.objects.create(
#                 location=countryrow.location,
#                 date=countryrow.date,
#                 p_scores_all_ages=countryrow.p_scores_all_ages,
#                 p_scores_15_64=countryrow.p_scores_15_64,
#                 p_scores_65_74=countryrow.p_scores_65_74,
#                 p_scores_75_84=countryrow.p_scores_75_84,
#                 p_scores_85plus=countryrow.p_scores_85plus,
#                 deaths_2020_all_ages=countryrow.deaths_2020_all_ages,
#                 average_deaths_2015_2019_all_ages=countryrow.average_deaths_2015_2019_all_ages,
#                 deaths_2015_all_ages=countryrow.deaths_2015_all_ages,
#                 deaths_2016_all_ages=countryrow.deaths_2016_all_ages,
#                 deaths_2017_all_ages=countryrow.deaths_2017_all_ages,
#                 deaths_2018_all_ages=countryrow.deaths_2018_all_ages,
#                 deaths_2019_all_ages=countryrow.deaths_2019_all_ages,
#                 deaths_2010_all_ages=countryrow.deaths_2010_all_ages,
#                 deaths_2011_all_ages=countryrow.deaths_2011_all_ages,
#                 deaths_2012_all_ages=countryrow.deaths_2012_all_ages,
#                 deaths_2013_all_ages=countryrow.deaths_2013_all_ages,
#                 deaths_2014_all_ages=countryrow.deaths_2014_all_ages,
#                 Week=countryrow.Week,
#                 deaths_2021_all_ages=countryrow.deaths_2021_all_ages
#             )
#
#     def return_mortdf(self):
#         return self.dfMort
#
#
# class SummaryDF:
#     def __init__(self):
#         self.dfToGroup = NewDataFrame().return_df()
#         self.groupDf = pd.DataFrame(self.dfToGroup).groupby('Country', as_index=False).max('Date')
#
#     def return_sumdf(self):
#         return self.groupDf
#
#
# class VacDataFrame:
#     def __init__(self):
#         self.urlVacc = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv"
#         self.fileVacc = pd.read_csv(self.urlVacc)
#         self.dfVacc = pd.DataFrame(self.fileVacc,
#                                    columns=['location', 'iso_code', 'date', 'total_vaccinations', 'people_vaccinated',
#                                             'people_fully_vaccinated', 'daily_vaccinations'])
#         self.dfVacc = self.dfVacc.rename(columns={
#             'location': 'Country',
#             'date': 'Date',
#             'total_vaccinations': 'Total vaccinations',
#             'people_vaccinated': 'People vaccinated',
#             'people_fully_vaccinated': 'People fully vaccinated',
#             'daily_vaccinations': 'Daily vaccinations'
#         })
#
#     def vaccinfo(self):
#         return self.dfVacc.info(verbose=True)
#
#     def return_vacdf(self):
#         return self.dfVacc
#

class CreateFeather(NewDataFrame):
    def __init__(self):
        self.featherFile = 'main.ftr'
        self.myDataFrame = NewDataFrame().return_df()
        self.myDataFrame.reset_index().to_feather(self.featherFile)
