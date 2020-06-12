import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

def getTreemap(value=1970):
    df = pd.read_csv("data/weapons.csv")
    df_year = df.loc[df['year'] == value]
    df_slide = df['year'].unique()

    fig = px.treemap(df_year,
                     path=['year', 'weapon_type'],
                     values='quantity', title='Teste',
                     width=500, height=500
                     )

    fig.update_layout(
        font_family="Arial",
        margin=dict(
            l=0,
            r=75,
            b=0,
            t=0,
            pad=0,
        ),
        plot_bgcolor='rgb(30,30,30)',
        paper_bgcolor='rgb(30,30,30)',
    )

    return fig
