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
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import treemap as treemap




app = dash.Dash(__name__, assets_folder='style',external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container([
    html.H1("Terrorism around the world (1970-2017)", className="w-100 p-3 text-left"),
    #dbc.Row(dbc.Col(html.Div("Start"),width={"size": 12, "offset": 0})),
    dbc.Row(
        [
            dbc.Col([
                dbc.Row(
                    html.P( "text text text text text text text text text text text text text text text text text"
                            " text text text text text text text text text text text text text text text text text text"
                            " text text text text text text text text text text text text text text text text text text"
                            " text text text text text text text text text text text text text text text text text text"
                            " text text text text text text text text text text text text text text text text text text"
                            " text text text text text text text text text text text text text text text text text text"
                            " text text text text text text text text text text text text text text text text text text"
                            " text text text text text text text text text text", className="p-4 text-justify"),
                ),
                dbc.Row(
                    html.Div([

                        dcc.Graph(figure=treemap.getTreemap(), id='mytree', className="p-3"),

                        html.Label('Year'),
                        dcc.Slider(
                            id='year_slider',
                            min=1970,
                            max=2017,
                            marks={1970: '1970', 1975: '1975', 1980: '1980', 1985: '1985', 1990: '1990', 1995: '1995',
                                   2000: '2000', 2005: '2005', 2010: '2010', 2017: '2017'},
                            value=1970,
                            step=1,
                            included=False,
                            className='p-3'
                        ),
                    ])
                )
            ], width=3, className="p-4"),
            dbc.Col(
                 dcc.Graph(
                     id='fig',
                     figure=map.fig
                 )
            ,width=9)
        ]
        ),
    dbc.Row(
        [
            #dbc.Col(dcc.Graph(figure=treemap.fig, id='mytree'), width=3),
            dbc.Col([
                dbc.Row(
                    dcc.Graph(id='bar_plot',figure=stacked.figure)
                ),
                dbc.Row([
                     html.Div(id='evolution-Graphs-content'),
                     dcc.Tabs(id='evolution_Graphs', value='DeathsOverTotalDeaths', vertical=True, children=[
                         dcc.Tab(label='DeathsOverTotalDeaths', value='DeathsOverTotalDeaths'),
                         dcc.Tab(label='DeathsByRegion', value='DeathsByRegion'),
                         ]),

                    ])
                ], width=9
                ),
            ],no_gutters=True,
        )
    ]
    ,fluid=True)

@app.callback(Output('evolution-Graphs-content', 'children'),
              [Input('evolution_Graphs', 'value')])
def render_content(tab):
    if tab == 'DeathsOverTotalDeaths':
        return dcc.Graph(
                         id='fig2',
                         figure=deathsvstotaldeaths.DeathOverDeathFig,
                         animate=False
                     )
    elif tab == 'DeathsByRegion':
        return dcc.Graph(id='killsByRegion',
                   config={'displayModeBar': False},
                   animate=True,
                   figure=px.line(deathsvstotaldeaths.killsByRegionDF,
                                  x='Year',
                                  y='NumDeaths',
                                  color='Region',
                                  template='plotly_dark')
                          )

@app.callback([Output('mytree', 'figure')],
              [Input('year_slider', 'value')])
def update_graph(value):
    return treemap.getTreemap(value)

if __name__ == '__main__':
    app.run_server(debug=True)
