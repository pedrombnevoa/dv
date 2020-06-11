import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import os
import numpy as np
import map as map

#Miguel

YearGangKillsPath = os.getcwd() + '\GroupedYearGangKills.csv'

columns = ['Year','Organization','NumDeaths']

killsByGangDF = pd.read_csv(YearGangKillsPath, encoding='ISO-8859-1', usecols=columns)


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
                                        )
])


if __name__ == '__main__':
    app.run_server(debug=True)
