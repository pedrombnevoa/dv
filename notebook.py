import pandas as pd
import os

# ds = 'https://media.githubusercontent.com/media/pedrombnevoa/dv/master/globalterrorismdb_0718dist.csv'
ds = os.getcwd() + '\globalterrorismdb_0718dist.csv'

fields = ['eventid', 'iyear', 'country_txt', 'region_txt', 'city', 'latitude', 'longitude', 'nkill']

df = pd.read_csv(ds, encoding='ISO-8859-1', usecols=fields)
print(df.head(1))
