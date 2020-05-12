import pandas as pd
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import numpy as np

ds = 'https://media.githubusercontent.com/media/pedrombnevoa/dv/master/globalterrorismdb_0718dist.csv'
#ds = os.getcwd() + '\globalterrorismdb_0718dist.csv'

fields = ['eventid', 'iyear', 'country_txt', 'region_txt', 'city', 'latitude', 'longitude', 'nkill']

df = pd.read_csv(ds, encoding='ISO-8859-1', usecols=fields)

data_choropleth = dict(type='choropleth',
                       locations=df['country_txt'],
                       locationmode='country names',
                       z=np.log(df['nkill']),
                       text=df['country_txt'],
                       colorscale='inferno',
                       colorbar=dict(title='Deaths caused by terrorist attacks log scaled')
                      )

layout_choropleth = dict(geo=dict(scope='world',  # default
                                  projection=dict(type='orthographic'
                                                  ),
                                  # showland=True,   # default = True
                                  landcolor='black',
                                  lakecolor='white',
                                  showocean=True,  # default = False
                                  oceancolor='azure'
                                  ),

                         title=dict(text='World Choropleth Map',
                                    x=.5  # Title relative position according to the xaxis, range (0,1)
                                    )
                         )

fig = go.Figure(data=data_choropleth, layout=layout_choropleth)

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div(children=[
    html.H1(children='Test2'),

    html.Div(children='''
        Example of html Container
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)