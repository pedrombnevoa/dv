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
                dcc.Markdown(
                    'This dashboard presents a comprehensive set of '
                    'insights about terrorism around the world and '
                    'shows its evolution over the last decades, '
                    'regarding the most affected regions, the main '
                    'groups and organizations, the most used weapons '
                    'that were used and how many victims occurred '
                    'during these attacks.\n\n'
                    'According to the FBI, terrorism is "the unlawful '
                    'use of force or violence against persons or '
                    'property to intimidate or coerce a government, ' 
                    'the civilian population, or any segment thereof, '
                    'in furtherance of political or social objectives.\n\n'
                    'You can explore more of the global terrorism database by visiting this [link]('
                    'https://www.kaggle.com/START-UMD/gtd).'' \
                    ', className='p-3 text-justify shadow-5 markdown')
            ], className='pl-3'),

            dbc.Row([
                html.Div([
                    dcc.Graph(figure=treemap.fig, id='mytree'),

                    dcc.Slider(
                        id='year_slider',
                        min=1970,
                        max=2017,
                        marks={1970: {'label': '1970', 'style': {'color': '#ededed'}},
                               1975: {'label': '1975', 'style': {'color': '#ededed'}},
                               1980: {'label': '1980', 'style': {'color': '#ededed'}},
                               1985: {'label': '1985', 'style': {'color': '#ededed'}},
                               1990: {'label': '1990', 'style': {'color': '#ededed'}},
                               1995: {'label': '1995', 'style': {'color': '#ededed'}},
                               2000: {'label': '2000', 'style': {'color': '#ededed'}},
                               2005: {'label': '2005', 'style': {'color': '#ededed'}},
                               2010: {'label': '2010', 'style': {'color': '#ededed'}},
                               2017: {'label': '2017', 'style': {'color': '#ededed'}}},
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
                html.Div([
                    dcc.Graph(
                        id='fig2',
                        figure=deathsvstotaldeaths.DeathOverDeathFig,
                        animate=False
                    ),
                ], id='evolution-Graphs-content', className='shadow-5 pl-3'),
            ], className='pl-3')
        ], width=6, className="pt-2"),
    ], className='pt-2'),

    dbc.Row([
        dbc.Col([
            dbc.Row([
                html.Div(
                dcc.Graph(id='killsByRegion',
                    config={'displayModeBar': False},
                    animate=False,
                    figure=deathsvstotaldeaths.DeathsByRegion
                          ),className='shadow-5'
                )
                ], className='pl-3'
            )
            ], className="pt-2"
        )
    ], className='pt-2'),

    dbc.Row([
        dbc.Col([
            dbc.Row([
                dcc.Markdown('Project by Pedro Névoa, Pedro Santos, Ricardo Cardoso, Vítor Miguel Fernandes (NOVA IMS '
                             '2020)', className='p-2 text-right shadow-5 markdown')
            ], className='pl-3')
        ], className='pt-2')
    ], className='pt-2 pb-3')

],fluid=True)

@app.callback([Output('mytree', 'figure')],
              [Input('year_slider', 'value')])
def update_graph(value):
    df_year = treemap.df.loc[treemap.df['year'] == value]
    fig = treemap.px.treemap(df_year,
                    path=['year', 'weapon_type'],
                    values='quantity',
                    width=425, height=317,
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
            t=50,
            pad=0,
        ),
        plot_bgcolor='rgb(30,30,30)',
        paper_bgcolor='rgb(30,30,30)',
        title = dict(text='Most used types of weapons',
                 font=dict(color='#ededed', family='sans-serif'), x=0)
    )

    return [fig]

if __name__ == '__main__':
    app.run_server(debug=True)
