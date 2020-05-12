import pandas as pd
import os
import dash
import dash_core_components as dcc
import dash_html_components as html

ds = 'https://media.githubusercontent.com/media/pedrombnevoa/dv/master/globalterrorismdb_0718dist.csv'
#ds = os.getcwd() + '\globalterrorismdb_0718dist.csv'

fields = ['eventid', 'iyear', 'country_txt', 'region_txt', 'city', 'latitude', 'longitude', 'nkill']

df = pd.read_csv(ds, encoding='ISO-8859-1', usecols=fields)

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div(children=[
    html.H1(children='My First DashBoard'),

    html.Div(children='''
        Example of html Container
    '''),

    dcc.Graph(
        id='example-graph',
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)