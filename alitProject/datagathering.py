import pandas as pd
from Covid.models import CovidDataSet, Country, Mortality
from decimal import Decimal, DecimalException

pd.set_option('use_inf_as_na', True)


class NewDataFrame:
    def __init__(self):
        self.urlAggr = pd.read_csv(
            "https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv", parse_dates=True)
        self.urlRef = pd.read_csv("https://raw.githubusercontent.com/datasets/covid-19/main/data/reference.csv",
                                  parse_dates=True)
        self.urlTests = pd.read_csv(
            "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/testing/covid-testing-all-observations.csv",
            parse_dates=True)
        self.dfAggr = pd.DataFrame(self.urlAggr)
        self.dfref = pd.DataFrame(self.urlRef,
                                  columns=['iso2', 'iso3', 'Province_State', 'Country_Region', 'Population'])
        self.dfref = self.dfref[self.dfref['Province_State'].isnull()]
        self.dfTests = pd.DataFrame(self.urlTests)
        self.dfAux = pd.DataFrame.merge(self.dfAggr, self.dfref, how='left', left_on=['Country'],
                                        right_on=['Country_Region'])
        columns = ['Province_State', 'Country_Region']
        self.dfAux = self.dfAux.drop(columns, axis=1)
        keywords = ['people', 'performed']
        self.dfTests = self.dfTests[self.dfTests['Entity'].str.contains('|'.join(keywords))]
        self.dfTests = self.dfTests.drop_duplicates(['Date', 'ISO code'])
        self.dfComplete = pd.merge(self.dfAux, self.dfTests, how='left', left_on=['Date', 'iso3'],
                                   right_on=['Date', 'ISO code'])
        self.dfComplete.sort_values(by=['Country', 'Date'])
        self.dfComplete = self.dfComplete[self.dfComplete['Population'] > 0]
        columns = ['Entity', 'ISO code', 'Source URL',
                   'Source label', 'Notes', 'Cumulative total', 'Cumulative total per thousand',
                   'Daily change in cumulative total per thousand', '7-day smoothed daily change',
                   '7-day smoothed daily change per thousand', 'Short-term positive rate', 'Short-term tests per case']
        self.dfComplete = self.dfComplete.drop(columns, axis=1)
        self.dfComplete = self.dfComplete.rename(
            columns={
                'Daily change in cumulative total': 'Daily_tests'
            })
        self.dfComplete['Date'] = pd.to_datetime(self.dfComplete['Date'])
        self.dfComplete.sort_values(by=['Date'])
        self.dfComplete['Daily_cases'] = self.dfComplete.groupby(['Country'], group_keys=False)[
            "Confirmed"].diff().fillna(0)
        self.dfComplete['Daily_recovered'] = self.dfComplete.groupby(['Country'], group_keys=False)[
            "Recovered"].diff().fillna(0)
        self.dfComplete['Daily_deaths'] = self.dfComplete.groupby(['Country'], group_keys=False)[
            "Deaths"].diff().fillna(0)
        self.dfComplete['Active_cases'] = self.dfComplete['Confirmed'] - (
                self.dfComplete['Recovered'] + self.dfComplete['Deaths'])
        self.dfComplete['Active_per_100k'] = round(
            (self.dfComplete['Active_cases'] / self.dfComplete['Population']) * 100000, 2)
        self.dfComplete['Daily_cases_smooth'] = round(
            self.dfComplete.groupby(['Country'], group_keys=False)["Daily_cases"].rolling(window=7).mean().reset_index(
                0, drop=True), 2).fillna(0)
        self.dfComplete['Daily_deaths_smooth'] = round(
            self.dfComplete.groupby(['Country'], group_keys=False)["Daily_deaths"].rolling(window=7).mean().reset_index(
                0, drop=True), 2).fillna(0)
        self.dfComplete['Positive_test_rate'] = round(
            (self.dfComplete['Daily_cases'] / self.dfComplete['Daily_tests']).fillna(0), 2)
        self.dfComplete['Tests_performed'] = self.dfComplete.groupby(['Country'], group_keys=False)[
            "Daily_tests"].cumsum()
        self.dfComplete['Tests_per_case'] = round(
            (self.dfComplete['Daily_tests'] / self.dfComplete['Daily_cases']).fillna(0), 2)
        self.dfComplete['Tests_per_case'] = self.dfComplete['Tests_per_case'].fillna(0)
        self.dfComplete['Case_fatality'] = round(self.dfComplete['Deaths'] / self.dfComplete['Confirmed'], 2).fillna(0)
        self.dfComplete['Incidence_rate'] = round(self.dfComplete['Confirmed'] / self.dfComplete['Population'],
                                                  2).fillna(0)
        self.dfComplete['Confirmed'] = self.dfComplete['Confirmed'].astype('int32')
        self.dfComplete['Recovered'] = self.dfComplete['Recovered'].astype('int32')
        self.dfComplete['Deaths'] = self.dfComplete['Deaths'].astype(str).replace('', 0).astype('int32')
        self.dfComplete['Population'] = self.dfComplete['Population'].astype('int32')
        self.dfComplete['Daily_tests'] = self.dfComplete['Daily_tests'].fillna(0).astype('int32')
        self.dfComplete['Tests_performed'] = self.dfComplete['Tests_performed'].fillna(0).astype('int32')

    def writetodb(self):
        CovidDataSet.objects.all().delete()
        for dfrow in self.dfComplete.itertuples():
            try:
                dfrow = CovidDataSet.objects.create(
                    Date=dfrow.Date,
                    Country=dfrow.Country,
                    Confirmed=dfrow.Confirmed,
                    Recovered=dfrow.Recovered,
                    Deaths=dfrow.Deaths,
                    iso2=dfrow.iso2,
                    iso3=dfrow.iso3,
                    Population=dfrow.Population,
                    Daily_cases=dfrow.Daily_cases,
                    Daily_recovered=dfrow.Daily_recovered,
                    Daily_deaths=dfrow.Daily_deaths,
                    Active_cases=dfrow.Active_cases,
                    Active_per_100k=dfrow.Active_per_100k,
                    Daily_cases_smooth=dfrow.Daily_cases_smooth,
                    Daily_deaths_smooth=dfrow.Daily_deaths_smooth,
                    Daily_tests=dfrow.Daily_tests,
                    Positive_test_rate=dfrow.Positive_test_rate,
                    Tests_per_case=dfrow.Tests_per_case,
                    Case_fatality=dfrow.Case_fatality,
                    Incidence_rate=dfrow.Incidence_rate
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


class ExcessMort:
    def __init__(self):
        self.urlMort = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/excess_mortality/excess_mortality.csv"
        self.fileMort = pd.read_csv(self.urlMort)
        self.dfMort = pd.DataFrame(self.fileMort)
        self.dfMort = self.dfMort.fillna(0)

    def writetodb(self):
        Mortality.objects.all().delete()
        for countryrow in self.dfMort.itertuples():
            countryrow = Mortality.objects.create(
                location=countryrow.location,
                date=countryrow.date,
                p_scores_all_ages=countryrow.p_scores_all_ages,
                p_scores_15_64=countryrow.p_scores_15_64,
                p_scores_65_74=countryrow.p_scores_65_74,
                p_scores_75_84=countryrow.p_scores_75_84,
                p_scores_85plus=countryrow.p_scores_85plus,
                deaths_2020_all_ages=countryrow.deaths_2020_all_ages,
                average_deaths_2015_2019_all_ages=countryrow.average_deaths_2015_2019_all_ages,
                deaths_2015_all_ages=countryrow.deaths_2015_all_ages,
                deaths_2016_all_ages=countryrow.deaths_2016_all_ages,
                deaths_2017_all_ages=countryrow.deaths_2017_all_ages,
                deaths_2018_all_ages=countryrow.deaths_2018_all_ages,
                deaths_2019_all_ages=countryrow.deaths_2019_all_ages,
                deaths_2010_all_ages=countryrow.deaths_2010_all_ages,
                deaths_2011_all_ages=countryrow.deaths_2011_all_ages,
                deaths_2012_all_ages=countryrow.deaths_2012_all_ages,
                deaths_2013_all_ages=countryrow.deaths_2013_all_ages,
                deaths_2014_all_ages=countryrow.deaths_2014_all_ages,
                Week=countryrow.Week,
                deaths_2021_all_ages=countryrow.deaths_2021_all_ages
            )

    def return_mortdf(self):
        return self.dfMort


class SummaryDF:
    def __init__(self):
        self.dfToGroup = NewDataFrame().return_df()
        self.groupDf = pd.DataFrame(self.dfToGroup).groupby('Country', as_index=False).max('Date')

    def return_sumdf(self):
        return self.groupDf


class VacDataFrame:
    def __init__(self):
        self.urlVacc = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv"
        self.fileVacc = pd.read_csv(self.urlVacc)
        self.dfVacc = pd.DataFrame(self.fileVacc,
                                   columns=['location', 'iso_code', 'date', 'total_vaccinations', 'people_vaccinated',
                                            'people_fully_vaccinated', 'daily_vaccinations'])
        self.dfVacc = self.dfVacc.rename(columns={
            'location': 'Country',
            'date': 'Date',
            'total_vaccinations': 'Total vaccinations',
            'people_vaccinated': 'People vaccinated',
            'people_fully_vaccinated': 'People fully vaccinated',
            'daily_vaccinations': 'Daily vaccinations'
        })

    def vaccinfo(self):
        return self.dfVacc.info(verbose=True)

    def return_vacdf(self):
        return self.dfVacc


class CreateFeather(NewDataFrame):
    def __init__(self):
        self.featherFile = 'main.ftr'
        self.myDataFrame = NewDataFrame().return_df()
        self.myDataFrame.reset_index().to_feather(self.featherFile)



