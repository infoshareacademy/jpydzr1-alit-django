from django_plotly_dash import DjangoDash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from countryinfo import CountryInfo
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


app = DjangoDash('SimpleExample')
#server = app.server

pd.set_option('use_inf_as_na', True)

def getNewData():
    csvFile = pd.read_csv("https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv", parse_dates=True)
    testsCsvFile = pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/testing/covid-testing-all-observations.csv")
    countryISOcsv = pd.read_csv("allcodes.csv")
    exessMortFile = pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/excess_mortality/excess_mortality.csv")
    vaccFile = pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv", parse_dates=True)
    global completeSet
    global sumCases
    global listOfCountries
    global excessMortSet
    global vaccSet
    # Read source cvs files
    def createCountryList(dataFile):
        countryList = pd.DataFrame(dataFile).Country.unique()
        countryList = countryList.tolist()
        return countryList
    listOfCountries = createCountryList(csvFile)
    # Generate simple dataframe with country population data
    populationRows = []
    for country in listOfCountries:
        try:
            populationRows.append([country, CountryInfo(country).population()])
        except:
            pass
    populationSet = pd.DataFrame(populationRows, columns=["Country", "population"])
    countryISOdf = pd.DataFrame(countryISOcsv)
    countryRawData = pd.DataFrame(csvFile)
    vaccSet = pd.DataFrame(vaccFile)
    countryISOdf.loc[countryISOdf['Country'] == 'United Kingdom of Great Britain and Northern Ireland', 'Country'] = "United Kingdom"
    countryISOdf.loc[countryISOdf['Country'] == 'Iran (Islamic Republic of)', 'Country'] = "Iran"
    countryISOdf.loc[countryISOdf['Country'] == 'Bolivia (Plurinational State of)', 'Country'] = "Bolivia"
    countryISOdf.loc[countryISOdf['Country'] == 'Brunei Darussalam', 'Country'] = "Brunei"
    countryISOdf.loc[countryISOdf['Country'] == 'Korea, Republic of', 'Country'] = "Korea, South"
    countryISOdf.loc[countryISOdf['Country'] == 'Moldova, Republic of', 'Country'] = "Moldova"
    countryISOdf.loc[countryISOdf['Country'] == 'Russian Federation', 'Country'] = "Russia"
    countryISOdf.loc[countryISOdf['Country'] == 'Syrian Arab Republic', 'Country'] = "Syria"
    countryISOdf.loc[countryISOdf['Country'] == 'United States of America', 'Country'] = "US"
    countryISOdf.loc[countryISOdf['Country'] == 'Venezuela (Bolivarian Republic of)', 'Country'] = "Venezuela"
    countryISOdf.loc[countryISOdf['Country'] == 'Viet Nam', 'Country'] = "Vietnam"
    testPerf = pd.DataFrame(testsCsvFile).drop_duplicates(['Date', 'ISO code'])
    mergedISO = pd.merge(countryRawData, countryISOdf, how='left', on=['Country'])
    completeSet = pd.merge(mergedISO, testPerf, how='left', on=['ISO code', 'Date'])
    completeSet = pd.merge(completeSet, populationSet, how='left', on=['Country'])
    # completeSet['population'] = pypopulation.get_population(str(completeSet['alpha-2']))
    completeSet.sort_values(by=['Date'])
    completeSet['Date'] = pd.to_datetime(completeSet['Date'])
    completeSet['year'] = completeSet['Date'].dt.year
    completeSet['month'] = completeSet['Date'].dt.month
    completeSet['dateDiff'] = pd.to_numeric((completeSet['Date'] - completeSet['Date'].min()).dt.days)
    completeSet['WeekOfYear'] = completeSet['Date'].dt.isocalendar().week
    completeSet['Active'] = completeSet['Confirmed'] - (completeSet['Recovered'] + completeSet['Deaths'])
    completeSet['New cases'] = pd.to_numeric(completeSet.groupby(['Country'], group_keys=False)["Confirmed"].diff().fillna(0))
    completeSet['dailyRecovered'] = completeSet.groupby(['Country'], group_keys=False)["Recovered"].diff().fillna(0)
    completeSet['Daily deaths'] = completeSet.groupby(['Country'], group_keys=False)["Deaths"].diff().fillna(0)
    completeSet['cases7dRa'] = round(completeSet.groupby(['Country'], group_keys=False)["New cases"].rolling(window=7).mean().reset_index(0, drop=True).fillna(0), 2)
    completeSet['deaths7dRa'] = round(completeSet.groupby(['Country'], group_keys=False)["Daily deaths"].rolling(window=7).mean().reset_index(0,drop=True).fillna(0), 2)
    completeSet['positiveTestRate'] = round((completeSet['New cases'] / completeSet['Daily change in cumulative total']).fillna(0), 2)
    completeSet['testsPerCase'] = round((completeSet['Daily change in cumulative total'] / completeSet['New cases']).fillna(0), 2)
    completeSet['Case fatality'] = round((completeSet['Deaths'] / completeSet['Confirmed']).fillna(0), 4)
    completeSet['nCasesPM'] = round((completeSet['New cases'] / completeSet['population']) * 1000000)
    completeSet['nRecoveredPM'] = ((completeSet['dailyRecovered'] / completeSet['population']) * 1000000)
    completeSet['cases7dRaPM'] = round((completeSet['cases7dRa'] / completeSet['population']) * 1000000)
    completeSet['Incidence rate'] = round((completeSet['Confirmed'] / completeSet['population']) * 100000, 2)
    completeSet['Mortality'] = round((completeSet['Deaths'] / completeSet['population']) * 100000, 2)
    completeSet['Case fatality'] = round((completeSet['Deaths']/completeSet['Confirmed']), 4)
    completeSet['Active per 100k'] = round((completeSet['Active']/completeSet['population']) * 100000, 2)
    columns = ['Entity', 'Source URL', 'Source label', 'Notes', 'Cumulative total', 'Cumulative total per thousand',
               'Daily change in cumulative total per thousand', '7-day smoothed daily change',
               '7-day smoothed daily change per thousand', 'Short-term tests per case', 'Short-term positive rate']
    completeSet.drop(columns, inplace=True, axis=1)
    #completeSet.to_csv('set.csv')
    #completeSet.to_feather('set.feather')
    sumCases = pd.DataFrame(completeSet).groupby('Country', as_index=False).max('Date')
    sumCases['Case fatality'] = round(sumCases['Deaths'] / sumCases['Confirmed'], 4)
    excessMortSet = pd.DataFrame(exessMortFile).rename(columns={'location': 'Country', 'date': 'Date'})
    vaccSet.drop(['daily_vaccinations', 'total_vaccinations_per_hundred', 'daily_vaccinations_per_million'], inplace=True, axis=1)
    vaccSet = vaccSet.dropna(subset=['total_vaccinations'])
    vaccSet['Daily Vaccinations'] = pd.to_numeric(vaccSet.groupby(['location'], group_keys=False)['total_vaccinations'].diff().fillna(0))

getNewData()


app.layout = html.Div([
    html.H1('Simple graph example'),
    dcc.Dropdown(
        id='continentsDropdown',
        options=[
            {'label': 'World', 'value': 'world'},
            {'label': 'Europe', 'value': 'europe'},
            {'label': 'Asia', 'value': 'asia'},
            {'label': 'Africa', 'value': 'africa'},
            {'label': 'North America', 'value': 'north america'},
            {'label': 'South America', 'value': 'south america'},
        ],
        value='world',
        multi=False
    ),
    dcc.Graph(id='graph1')
])

@app.callback(
    Output('graph1', 'figure'),
    [Input('continentsDropdown', 'value')])
def update_figure(selected_value):
    filtered_df = sumCases
    fig3 = px.choropleth(filtered_df, locations="Country",
                         color="Case fatality",
                         scope=selected_value,
                         hover_name="Case fatality",
                         locationmode="country names",
                         range_color=[0, 0.15],
                         color_continuous_scale=px.colors.sequential.matter, )
    fig3.update_layout(transition_duration=500,
                       template="plotly_white",
                       margin=dict(t=0, b=0, l=0, r=0),
                       )
    return fig3
