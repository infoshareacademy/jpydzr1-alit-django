import pandas as pd

pd.set_option('use_inf_as_na', True)


class NewDataFrame:
    def __init__(self):
        self.urlAggr = "https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv"
        self.urlRef = "https://raw.githubusercontent.com/datasets/covid-19/main/data/reference.csv"
        self.urlTests = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/testing/covid-testing-all-observations.csv"
        self.fileAggr = pd.read_csv(self.urlAggr)
        self.fileRef = pd.read_csv(self.urlRef)
        self.fileTests = pd.read_csv(self.urlTests)
        self.dfAggr = pd.DataFrame(self.fileAggr)
        self.dfRef = pd.DataFrame(self.fileRef,
                                  columns=['iso2', 'iso3', 'Province_State', 'Country_Region', 'Population'])
        self.dfRef = self.dfRef[self.dfRef['Province_State'].isnull()]
        self.dfTests = pd.DataFrame(self.fileTests)
        keywords = ['people', 'performed']
        self.dfTests = self.dfTests[self.dfTests['Entity'].str.contains('|'.join(keywords))]
        self.dfTests.drop_duplicates()
        self.dfAux = pd.merge(self.dfAggr, self.dfRef, how='left', left_on=['Country'], right_on=['Country_Region'])
        self.dfComplete = pd.merge(self.dfAux, self.dfTests, how='left', left_on=['Date', 'iso3'],
                                   right_on=['Date', 'ISO code'])
        columns = ['Province_State', 'Country_Region', 'Entity', 'ISO code', 'Source URL',
                   'Source label', 'Notes', 'Cumulative total', 'Cumulative total per thousand',
                   'Daily change in cumulative total per thousand', '7-day smoothed daily change',
                   '7-day smoothed daily change per thousand', 'Short-term positive rate', 'Short-term tests per case']
        self.dfComplete = self.dfComplete.drop(columns, axis=1)
        self.dfComplete = self.dfComplete[self.dfComplete['Population'] > 0]
        self.dfComplete = self.dfComplete.rename(
            columns={
                'Daily change in cumulative total': 'Daily tests'
            })
        self.dfComplete['Tests performed'] = self.dfComplete.groupby(['Country'])["Daily tests"].cumsum()
        self.dfComplete['Daily cases'] = self.dfComplete.groupby(['Country'])["Confirmed"].diff().fillna(0)
        self.dfComplete['Daily recovered'] = self.dfComplete.groupby(['Country'])["Recovered"].diff().fillna(0)
        self.dfComplete['Daily deaths'] = self.dfComplete.groupby(['Country'])["Deaths"].diff().fillna(0)
        self.dfComplete['Active cases'] = self.dfComplete['Confirmed'] - (
                    self.dfComplete['Recovered'] + self.dfComplete['Deaths'])
        self.dfComplete['Active per 100k'] = round(
            (self.dfComplete['Active cases'] / self.dfComplete['Population']) * 100000, 2)
        self.dfComplete['Daily cases smooth'] = round(
            self.dfComplete.groupby(['Country'])["Confirmed"].rolling(window=7).mean().reset_index(0, drop=True), 2)
        self.dfComplete['Daily deaths smooth'] = round(
            self.dfComplete.groupby(['Country'])["Daily deaths"].rolling(window=7).mean().reset_index(0, drop=True), 2)
        self.dfComplete['Positive test rate'] = round(
            (self.dfComplete['Daily cases'] / self.dfComplete['Daily tests']).fillna(0), 2)
        self.dfComplete['Tests per case'] = round(
            (self.dfComplete['Daily tests'] / self.dfComplete['Daily cases']).fillna(0), 2)
        self.dfComplete['Case fatality'] = round(self.dfComplete['Deaths'] / self.dfComplete['Confirmed'], 2)
        self.dfComplete['Incidence rate'] = round(self.dfComplete['Confirmed'] / self.dfComplete['Population'], 2)
        self.dfComplete['Date'] = pd.to_datetime(self.dfComplete['Date'])
        self.dfComplete['Confirmed'] = self.dfComplete['Confirmed'].astype('int32')
        self.dfComplete['Recovered'] = self.dfComplete['Recovered'].astype('int32')
        self.dfComplete['Deaths'] = self.dfComplete['Deaths'].astype(str).replace('', 0).astype('int32')
        self.dfComplete['Population'] = self.dfComplete['Population'].fillna(0).astype('int32')
        self.dfComplete['Daily tests'] = self.dfComplete['Daily tests'].fillna(0).astype('int32')
        self.dfComplete['Tests performed'] = self.dfComplete['Tests performed'].fillna(0).astype('int32')
        self.dfComplete['Daily cases'] = self.dfComplete['Daily cases'].astype('int16')
        self.dfComplete['Daily recovered'] = self.dfComplete['Daily recovered'].astype('int16')
        self.dfComplete['Daily deaths'] = self.dfComplete['Daily deaths'].astype('int16')
        self.dfComplete['Active cases'] = self.dfComplete['Active cases'].astype('int32')
        self.dfComplete['Active per 100k'] = self.dfComplete['Active per 100k'].astype('int16')
        self.dfComplete['Daily cases smooth'] = self.dfComplete['Daily cases smooth'].astype('float16')
        self.dfComplete['Daily deaths smooth'] = self.dfComplete['Daily deaths smooth'].astype('float16')
        self.dfComplete['Positive test rate'] = self.dfComplete['Positive test rate'].astype('float16')
        self.dfComplete['Tests per case'] = self.dfComplete['Tests per case'].astype('float16')
        self.dfComplete['Case fatality'] = self.dfComplete['Case fatality'].astype('float16')
        self.dfComplete['Incidence rate'] = self.dfComplete['Incidence rate'].astype('float16')

    def return_df(self):
        return self.dfComplete

    def df_info(self):
        return self.dfComplete.info(verbose=True)


class ExcessMort:
    def __init__(self):
        self.urlMort = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/excess_mortality/excess_mortality.csv"
        self.fileMort = pd.read_csv(self.urlMort)
        self.dfMort = pd.DataFrame(self.fileMort)

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


class CountryList:
    def __init__(self):
        self.dataFile = pd.read_csv("https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv", parse_dates=True)
        self.countryList = pd.DataFrame(self.dataFile).Country.unique()
        self.countryList = self.countryList.tolist()

    def return_coutrylist(self):
        return self.countryList

