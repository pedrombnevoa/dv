import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import os
import Stacked as stacked
import numpy as np
import map as map
import deathsvstotaldeathsChart as deathsvstotaldeaths

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
        figure=map.fig
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

    dcc.Graph(id='bar_plot',
              figure=stacked.figure

)

])


if __name__ == '__main__':
    app.run_server(debug=True)


