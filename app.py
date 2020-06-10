import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import os
import deathsvstotaldeathsChart as deathsvstotaldeaths

ds = os.getcwd() + '\globalterrorismdb_0718dist.csv'

fields = ['eventid', 'iyear', 'country', 'country_txt', 'region_txt', 'city', 'latitude', 'longitude', 'nkill']

df = pd.read_csv(ds, encoding='ISO-8859-1', usecols=fields)

df = df.loc[df['iyear'] >= 2000]

df['nkill'].fillna(0, inplace=True)

df = df.groupby(['country_txt', 'iyear'])['nkill'].sum().reset_index()
df = df.loc[df['nkill'] > 0]

data_slider = []

for i, year in enumerate(df.iyear.unique()):
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
        visible=True if i == 0 else False,
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
                size=12
            ),
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
    font=dict(
        family='Arial',
        size=12
    ),
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

#Miguel

YearGangKillsPath = os.getcwd() + '\GroupedYearGangKills.csv'

columns = ['Year','Organization','NumDeaths']

killsByGangDF = pd.read_csv(YearGangKillsPath, encoding='ISO-8859-1', usecols=columns)

killsByRegionDFPath = os.getcwd() + '\GroupedYearRegionKills.csv'

columnskillsByRegion = ['Region','Year','NumDeaths']
#Region,Year,NumDeaths
killsByRegionDF = pd.read_csv(killsByRegionDFPath, encoding='ISO-8859-1', usecols=columnskillsByRegion)

app = dash.Dash(__name__, assets_folder='style')
server = app.server

app.layout = html.Div(children=[
    # html.H1(children='Test2'),

    # html.Div(children='''
    #     Example of html Container
    # '''),

    dcc.Graph(
        id='fig',
        figure=fig
    ),
    dcc.Graph(id='timeseries',
              config={'displayModeBar': False},
              animate=True,
              figure=px.line(killsByGangDF,
                             x='Year',
                             y='NumDeaths',
                             color='Organization',
                             template='plotly_dark').update_layout(
                                       {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                        'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
                                        ),

    dcc.Graph(
            id='fig2',
            figure=deathsvstotaldeaths.DeathOverDeathFig,
            animate=False
        ),

    dcc.Graph(id='killsByGang',
              config={'displayModeBar': False},
              animate=True,
              figure=px.line(killsByGangDF,
                             x='Year',
                             y='NumDeaths',
                             color='Organization',
                             template='plotly_dark').update_layout(
                                       {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                        'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
                                        ),
    dcc.Graph(id='killsByRegion',
              config={'displayModeBar': False},
              animate=True,
              figure=px.line(killsByRegionDF,
                             x='Year',
                             y='NumDeaths',
                             color='Region',
                             template='plotly_dark').update_layout(
                                       {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                        'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
                                        ),
    dcc.Graph(id='attackvsdeaths',
              config={'displayModeBar': False},
              animate=True,
              figure=px.line(deathsvstotaldeaths.RegionYearAttackDeathsDF,
                             x='NumDeathsComul',
                             y='NumDeathsPerYear',
                             color='Region',
                             template='plotly_dark').update_layout(
                                       {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                        'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
                                        ),


])


if __name__ == '__main__':
    app.run_server(debug=True)
