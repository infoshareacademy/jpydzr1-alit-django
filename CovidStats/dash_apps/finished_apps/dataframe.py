import pandas as pd
import requests


class DataFrame:
    def __init__(self):
        self.url1 = "https://opendata.ecdc.europa.eu/covid19/casedistribution/json"
        self.file1 = requests.get(self.url1).json()
        self.file1 = self.file1['records']
        self.df = pd.DataFrame(data=self.file)

    def converter(self):
        self.df['cases'] = self.df['cases'].astype(int)
        self.df['deaths'] = self.df['deaths'].astype(int)
        self.df['popData2018'] = self.df['popData2018'].astype(str).replace('', 0).astype(int)
        self.df['dateRep'] = self.df['dateRep'].to_timestamp
        cols_rename = 'date day month year cases deaths country geo_id country_id population continent'.split()
        cols_rename = [s.capitalize() for s in cols_rename]
        self.df.columns = cols_rename

    def return_df(self):
        self.converter()
        return self.df
