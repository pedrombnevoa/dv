import pandas as pd
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import numpy as np
import random

ds = 'https://media.githubusercontent.com/media/pedrombnevoa/dv/master/globalterrorismdb_0718dist.csv'
# ds = os.getcwd() + '\globalterrorismdb_0718dist.csv'

fields = ['eventid', 'iyear', 'country', 'country_txt', 'region_txt', 'city', 'latitude', 'longitude', 'nkill']

df = pd.read_csv(ds, encoding='ISO-8859-1', usecols=fields)

df = df.loc[df['iyear'] >= 2000]

df['nkill'].fillna(0, inplace=True)

df = df.groupby(['country_txt', 'iyear'])['nkill'].sum().reset_index()
df = df.loc[df['nkill'] > 0]

data_slider = []

for year in df.iyear.unique():
    df_year = df[(df['iyear'] == year)]

    data_year = dict(
        type='choropleth',
        name='',
        colorscale='amp',
        locations=df_year['country_txt'],
        z=df_year['nkill'],
        zmax=15000,
        zmin=0,
        locationmode='country names',
        colorbar=dict(
            len=0.5,
            thickness=10,
            title=dict(
                text='Number of fatalities',
                font=dict(
                    family='Arial',
                    size=14,
                ),
                side='right'
            ),
            tickfont=dict(
                family='Arial',
                size=12),
        )
    )

    data_slider.append(data_year)

steps = []

for i in range(len(data_slider)):
    step = dict(
        method='restyle',
        args=['visible', [False] * len(data_slider)],
        label=(format(i + 2000))
    )

    step['args'][1][i] = True
    steps.append(step)

sliders = [dict(active=0, pad={"t": 1}, steps=steps)]

layout = dict(
    geo=dict(
        scope='world',
        showcountries=True,
        projection=dict(
            type='equirectangular'
        ),
        showland=True,
        landcolor='rgb(255, 255, 255)',
        showlakes=False,
        showrivers=False,
        showocean=True,
        oceancolor='white',
    ),
    sliders=sliders
)

fig = go.Figure(data=data_slider, layout=layout)

fig.update_layout(
    font=dict(family='Arial', size=12),
    autosize=False,
    width=1250,
    height=750,
    margin=dict(
        l=25,
        r=0,
        b=100,
        t=50,
        pad=0,
    )
)

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(children=[
    # html.H1(children='Test2'),

    # html.Div(children='''
    #     Example of html Container
    # '''),

    dcc.Graph(
        id='fig',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
