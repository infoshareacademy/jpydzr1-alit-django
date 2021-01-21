from django_plotly_dash import DjangoDash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from plotly.offline import plot
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from countryinfo import CountryInfo
import time
from datetime import datetime
from CovidStats.dash_apps.finished_apps.newdataframe import NewDataFrame, CreateFeather, CountryList, SummaryDF, ExcessMort, VacDataFrame
from CovidStats.models import CovidApi


app = DjangoDash('SimpleExample')

completeSet = NewDataFrame().return_df()
sumCases = SummaryDF().return_sumdf()
excessMortSet = ExcessMort().return_mortdf()
vaccSet = VacDataFrame().return_vacdf()
listOfCountries = CountryList().return_coutrylist()

print(sumCases[sumCases.Country == 'Poland']['Deaths'].to_string(index=False))

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
    dcc.Dropdown(
        id='countrydropdown',
        options=[{'label': name, 'value': name} for name in listOfCountries],
        value='Poland',
        clearable=False,
        multi=False
    ),
    dcc.Graph(id='graph1'),
    dcc.Graph(id='graph2'),
    dbc.Card(id='NC')
])

@app.callback(
    Output('NC', 'children'),
    [Input('countrydropdown', 'value')])
def update_card(selected_value):
    filtered_df = sumCases[sumCases.Country == selected_value]
    nc = filtered_df.iloc[0,1]
    print(nc)
    return nc

@app.callback(
    Output('graph1', 'figure'),
    [Input('continentsDropdown', 'value')])
def update_figure(selected_value):
    print('Continent')
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

@app.callback(
    Output('graph2', 'figure'),
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

@app.callback(
    Output('graph3', 'figure'),
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
    return plot(figure_or_data=fig3, include_plotlyjs=False, output_type='div')