import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

df = pd.read_csv("data/weapons.csv")
df_year = df.loc[df['year'] == 1970]
df_slide = df['year'].unique()

df = df[df['weapon_type'] != 'Unknown']

fig = px.treemap(df_year,
                 path=['year', 'weapon_type'],
                 values='quantity', #title='Teste',
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
    title=dict(text='Most used types of weapons',
               font=dict(color='white', family='sans-serif'), x=0)
)

##Layout
dcc.Graph(figure=fig, id='mytree'),

# dcc.Slider(
#     id='year_slider',
#     min=1970,
#     max=2017,
#     marks={str(i): '{}'.format(str(i)) for i in df_slide},
#     value=1970,
#     step=1,
#     included=False
# ),


# def getTreemap(value=1970):
#     df = pd.read_csv("data/weapons.csv")
#     df_year = df.loc[df['year'] == value]
#     df_slide = df['year'].unique()
#
#     fig = px.treemap(df_year,
#                      path=['year', 'weapon_type'],
#                      values='quantity', title='Teste',
#                      width=500, height=500
#                      )
#
#     fig.update_layout(
#         font_family="Arial",
#         margin=dict(
#             l=0,
#             r=75,
#             b=0,
#             t=0,
#             pad=0,
#         ),
#         plot_bgcolor='rgb(30,30,30)',
#         paper_bgcolor='rgb(30,30,30)',
#         colorscale=dict(sequential='amp')
#     )
#
#     return fig
