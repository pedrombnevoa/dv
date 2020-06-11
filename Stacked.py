import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import os

AttacksOverKillspath = os.getcwd() + '\globalterrorismdb_Attacks_Kills_Woumed.csv'

columns = ['Year','Attacks','Kills','Wound']

AttacksOverKillsDF = pd.read_csv(AttacksOverKillspath, encoding='ISO-8859-1', usecols=columns)

trace1 = go.Bar(
    x=AttacksOverKillsDF['Year'],
    y=AttacksOverKillsDF['Attacks'],
    name='Attacks',
    marker_color='rgb(171, 171, 170)'

)
trace2 = go.Bar(
    x=AttacksOverKillsDF['Year'],
    y=AttacksOverKillsDF['Kills'],
    name='Kills',
    marker_color='rgb(179, 0, 0)'
)
trace3 = go.Bar(
    x=AttacksOverKillsDF['Year'],
    y=AttacksOverKillsDF['Wound'],
    name='Wound',
    marker_color='rgb(255, 255, 0)'
)

annotations = [dict(
            x=1998,
            y=28000,
            xref="x",
            yref="y",
            text="Between 1997 and 2007, even with fewer attacks," 
                 "<br> in proportion these were the most deadly years",
            showarrow=True,
            font=dict(
                family="Arial, monospace",
                size=11,
                color='rgb(254, 254, 253)'
            ),
            align="center",
            xshift=-25,
            arrowhead=4,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor='rgb(224, 224, 223)',
            ax=-100,
            ay=-80,
            borderwidth=2,
            borderpad=4,
            bgcolor='rgb(179, 0, 0)',
            opacity=0.8
        )
    ]

annotations2 = [dict(
            x=2014,
            y=55000,
            xref="x",
            yref="y",
            text="In 2014 the Islamic State attack on an Iraqi prison in the city" 
                 "<br> of Mosul killed 670 prisoners, in the terrorist attack with"
                 "<br> the highest number of deaths since September 11, 2001",
            showarrow=True,
            font=dict(
                family="Arial, monospace",
                size=11,
                color='rgb(254, 254, 253)'
            ),
            align="center",
            xshift=-10,
            arrowhead=4,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor='rgb(224, 224, 223)',
            ax=-180,
            ay=0,
            borderwidth=2,
            borderpad=4,
            bgcolor='rgb(179, 0, 0)',
            opacity=0.8
        )
    ]

figure=go.Figure(
              data=[trace1, trace2, trace3],
              layout=go.Layout(
              xaxis_title="Year",
              xaxis={'categoryorder':'category ascending'},
              barmode='stack',
              annotations=annotations + annotations2,
              template='plotly_dark'))