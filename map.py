import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

ds = 'https://raw.githubusercontent.com/pedrombnevoa/dv/master/gt_country_year_nkill_count.csv'

df = pd.read_csv(ds, encoding='ISO-8859-1')

years = []
for year in df["year"]:
    if year not in years:
        years.append(year)

fig_dict = {
    "data": [],
    "layout": {},
    "frames": []
}

fig_dict["layout"]["updatemenus"] = [
    {
        "buttons": [
            {
                "args": [None, {"frame": {"duration": 500, "redraw": True},
                                "fromcurrent": True, "transition": {"duration": 300,
                                                                    "easing": "quadratic-in-out"}}],
                "label": "Play",
                "method": "animate"
            },
            {
                "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                  "mode": "immediate",
                                  "transition": {"duration": 0}}],
                "label": "Pause",
                "method": "animate"
            }
        ],
        "direction": "left",
        "pad": {"r": 10, "t": 10},
        "showactive": False,
        "type": "buttons",
        "x": 0.1,
        "xanchor": "right",
        "y": 0,
        "yanchor": "top",
        "font": {"family": "sans-serif", "color": "rgb(0, 0, 0)"}
    }
]

sliders_dict = {
    "active": 0,
    "yanchor": "top",
    "xanchor": "left",
    "currentvalue": {
        "font": {"size": 20},
        "prefix": "Year:",
        "visible": False,
        "xanchor": "right"
    },
    "transition": {"duration": 300, "easing": "cubic-in-out"},
    "pad": {"b": 10, "t": 0},
    "len": 0.9,
    "x": 0.1,
    "y": 0,
    "steps": [],
    "tickcolor": "#ededed",
    "font": {"family": "sans-serif", "color": "#ededed"}
}

df_year = df[(df['year'] == 1970)]

data_choropleth = dict(
    type='choropleth',
    name='',
    colorscale='amp',
    locations=df_year['country'],
    z=np.log(df_year['count']),
    meta=df_year['nkill'],
    customdata=df_year['count'],
    hovertemplate=
        df_year['country'] + '<br>' +
        '<b>%{customdata}</b> attacks <br>' +
        '<b>%{meta}</b> fatalities',
    zmax=10,
    zmin=0,
    locationmode='country names',
    colorbar=dict(
        outlinewidth=1,
        outlinecolor='#ededed',
        len=0.5,
        thickness=10,
        title=dict(
            text='Number of attacks (logarithmic scale)',
            font=dict(
                family='sans-serif',
                size=14,
                color='#ededed'
            ),
            side='right'
        ),
        tickfont=dict(
            family='sans-serif',
            size=12,
            color='#ededed'
        ),
    )
)

fig_dict["data"].append(data_choropleth)

for year in years:
    frame = {"data": [], "name": str(year)}

    df_year = df[(df['year'] <= year)]
    df_year1 = df_year.groupby(['country'])['count'].sum().reset_index()
    df_year2 = df_year.groupby(['country'])['nkill'].sum().reset_index()

    data_choropleth = dict(
        type='choropleth',
        name='',
        colorscale='amp',
        locations=df_year1['country'],
        z=np.log(df_year1['count']),
        meta=df_year2['nkill'],
        customdata=df_year1['count'],
        hovertemplate=
            df_year1['country'] + '<br>' +
            '<b>%{customdata}</b> attacks <br>' +
            '<b>%{meta}</b> fatalities',
        zmax=10,
        zmin=0,
        locationmode='country names',
        colorbar=dict(
            outlinewidth=1,
            outlinecolor='#ededed',
            len=0.5,
            thickness=10,
            title=dict(
                text='Number of attacks (logarithmic scale)',
                font=dict(
                    family='sans-serif',
                    size=14,
                    color='#ededed'
                ),
                side='right'
            ),
            tickfont=dict(
                family='sans-serif',
                size=12,
                color='#ededed'
            ),
        )
    )

    frame["data"].append(data_choropleth)

    fig_dict["frames"].append(frame)
    slider_step = {"args": [
        [year],
        {"frame": {"duration": 300, "redraw": True},
         "mode": "immediate",
         "transition": {"duration": 300}}
    ],
        "label": str(year),
        "method": "animate"}
    sliders_dict["steps"].append(slider_step)

fig_dict["layout"]["sliders"] = [sliders_dict]

fig = go.Figure(fig_dict)

fig.update_layout(
    font=dict(
        family='sans-serif',
        size=12
    ),
    autosize=False,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    width=1250,
    height=685,
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=50,
        pad=0,
    ),template= 'plotly_dark',
    geo=dict(
        scope='world',
        showcountries=True,
        projection=dict(
            type='equirectangular'
        ),
        showland=True,
        landcolor='rgb(255, 255, 255)',
        showlakes=False,
        showrivers=False,
        showocean=True,
        oceancolor='rgba(0,0,0,0)',
        showframe=False,
        framecolor='#ededed',
        bgcolor='rgb(30,30,30)'
    ),
    title=dict(text='Attacks and fatalities around the world', font=dict(family='sans-serif', color='#ededed'), x=0)
)
