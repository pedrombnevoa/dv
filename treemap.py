import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
from dash_html_components import H1

app = dash.Dash()
server = app.server

##Load Data
df = pd.read_csv("data/weapons.csv")
df_year = df.loc[df['year'] == 1970]
df_slide = df['year'].unique()

##First Treemap
fig = px.treemap(df_year,
                 path=['year', 'weapon_type'],
                 values='quantity', title='Teste',
                 width=500, height=500,
                 )
##Layout
app.layout = html.Div([

    H1('Type of Weapons Most Used'),

    dcc.Graph(figure=fig, id='mytree'),

    html.Label('Year Slider'),
    dcc.Slider(
        id='year_slider',
        min=1970,
        max=2017,
        marks={str(i): '{}'.format(str(i)) for i in df_slide},
        value=1970,
        step=1,
        included=False
    ),
])


##Callback Treemap
@app.callback([Output('mytree', 'figure')],
              [Input('year_slider', 'value')])
def update_graph(value):
    df_year = df.loc[df['year'] == value]
    fig = px.treemap(df_year,
                     path=['year', 'weapon_type'],
                     values='quantity', title='Type of Weapons Most Used',
                     width=500, height=500,
                     )

    return [fig]


if __name__ == '__main__':
    app.run_server(debug=True)
