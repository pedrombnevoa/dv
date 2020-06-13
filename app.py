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

    dbc.Row([
        dbc.Col([
            dbc.Row([
                html.H1("Terrorism around the world (1970-2017)", className="w-100 p-3 text-left shadow-5"),
            ], className="pt-3 pl-3"),
        ], width='auto'),
        dbc.Col()
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Row([
                dcc.Markdown('This dashboard offers a comprehensive insight into the numbers of terrorism around '
                            'the world. text text text text text text text text text text text text text text ['
                             'link](https://www.kaggle.com/START-UMD/gtd) text text text text text text text text '
                             'text text text text text text text text text text text text text text text text'
                             ' text text text text text text text text text text text text text text text text '
                             'text text ', className='p-2 text-justify shadow-5')
            ], className='pl-3'),

            dbc.Row([
                html.Div([
                    dcc.Graph(figure=treemap.fig, id='mytree'),

                    dcc.Slider(
                        id='year_slider',
                        min=1970,
                        max=2017,
                        marks={1970: {'label': '1970', 'style': {'color': 'white'}},
                               1975: {'label': '1975', 'style': {'color': 'white'}},
                               1980: {'label': '1980', 'style': {'color': 'white'}},
                               1985: {'label': '1985', 'style': {'color': 'white'}},
                               1990: {'label': '1990', 'style': {'color': 'white'}},
                               1995: {'label': '1995', 'style': {'color': 'white'}},
                               2000: {'label': '2000', 'style': {'color': 'white'}},
                               2005: {'label': '2005', 'style': {'color': 'white'}},
                               2010: {'label': '2010', 'style': {'color': 'white'}},
                               2017: {'label': '2017', 'style': {'color': 'white'}}},
                        value=1970,
                        step=1,
                        included=False,
                        className='w-100'
                    ),
                ], className='p-3 shadow-5')
            ], className='pl-3 pt-3')

        ], width=3, className="pt-2"),

        dbc.Col(
            dbc.Row([
                html.Div([
                    dcc.Graph(
                        id='fig',
                        figure=map.fig,
                    )
                ], className='p-3 shadow-5')
            ], className='pl-3')
        ,width=9, className="pt-2")
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Row([
                html.Div([
                    dcc.Graph(id='bar_plot', figure=stacked.figure)
                ], className='shadow-5')
            ], className='pl-3'),
        ], width=5, className="pt-2"),

        dbc.Col([
            dbc.Row([
                html.Div(id='evolution-Graphs-content', className='shadow-5', ),
                dcc.Tabs(
                    id='evolution_Graphs', value='DeathsOverTotalDeaths', vertical=False,
                    children=[
                        dcc.Tab(label='DeathsOverTotalDeaths', value='DeathsOverTotalDeaths'),
                        dcc.Tab(label='DeathsByRegion', value='DeathsByRegion'),
                    ]
                ),
            ], className='pl-3')
        ], width=5, className="pt-2"),
    ], className='pt-2')

],fluid=True)

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
                   animate=False,
                   figure=deathsvstotaldeaths.DeathsByRegion
                          )

# @app.callback([Output('mytree', 'figure')],
#               [Input('year_slider', 'value')])
# def update_graph(value):
#     return treemap.getTreemap(value)
@app.callback([Output('mytree', 'figure')],
              [Input('year_slider', 'value')])
def update_graph(value):
    df_year = treemap.df.loc[treemap.df['year'] == value]
    fig = treemap.px.treemap(df_year,
                     path=['year', 'weapon_type'],
                     values='quantity', title='Type of Weapons Most Used',
                     width=425, height=500,
                     color='quantity',
                     color_continuous_scale='amp'
                     )

    fig.update_layout(
        coloraxis=dict(showscale=False),
        font_family="Arial",
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=0,
        ),
        plot_bgcolor='rgb(30,30,30)',
        paper_bgcolor='rgb(30,30,30)'
        #colorscale=dict(sequential='amp')
    )

    return [fig]

if __name__ == '__main__':
    app.run_server(debug=True)
