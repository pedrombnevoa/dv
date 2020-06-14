import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html

killsByRegionDFPath = 'https://raw.githubusercontent.com/pedrombnevoa/dv/master/GroupedYearRegionKills.csv'
columnskillsByRegion = ['Region','Year','NumDeaths']
killsByRegionDF = pd.read_csv(killsByRegionDFPath, delimiter=',', encoding='ISO-8859-1', usecols=columnskillsByRegion)

RegionYearAttackDeathsPath = 'https://raw.githubusercontent.com/pedrombnevoa/dv/master/RegionYearDeathsDeathsCom.csv'
columnsRegionYearAttackDeaths = ['Region','Year','NumDeathsPerYear','NumDeathsComul','NumAttack']
RegionYearAttackDeathsDF = pd.read_csv(RegionYearAttackDeathsPath, encoding='ISO-8859-1', usecols=columnsRegionYearAttackDeaths)

years = ["1970", "1971", "1972", "1973", "1974", "1975", "1976", "1977", "1978", "1979",
         "1980", "1981", "1982", "1983", "1984", "1985", "1986", "1987", "1988", "1989",
         "1990", "1991", "1992", "1994", "1995", "1996", "1997", "1998", "1999",
        "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009",
        "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017"]

regions = []
for region in RegionYearAttackDeathsDF["Region"]:
    if region not in regions:
        regions.append(region)

fig_dict = {
    "data": [],
    "layout": {},
    "frames": []
}

fig_dict["layout"]["xaxis"] = {"range": [0, 5], "title": "Total deaths", "type": "log", "range": [-1, 5]}
fig_dict["layout"]["yaxis"] = {"range": [0, 5],"title": "Deaths last year", "type": "log", "range": [-1, 5]}
fig_dict["layout"]["hovermode"] = "closest"
fig_dict["layout"]["template"] = 'plotly_dark'
fig_dict["layout"]["height"] = 600
fig_dict["layout"]["width"] = 957

fig_dict["layout"]["updatemenus"] = [
    {
        "buttons": [
            {
                "args": [None, {"frame": {"duration": 500, "redraw": False},
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
        "pad": {"r": 10, "t": 87},
        "showactive": False,
        "type": "buttons",
        "x": 0.1,
        "xanchor": "right",
        "y": 0,
        "yanchor": "top",
        "font": {"color":'rgb(0, 0, 0)', "size":14}
    },
    {
        "buttons": [
            {
                "label": "Log",
                "method": "relayout",
                "args": [
                    {
                     'yaxis': {"title": "Deaths last year Log Scale", 'type': 'log', "range": [-1, 5]},
                     'xaxis': {"title": "Total deaths Log Scale", 'type': 'log', "range": [-1, 5]}}]
            },
            {
                "label": "Linear",
                "method": "relayout",
                "args": [
                    {
                     'xaxis': {"title": "Deaths last year Linear Scale", 'type': 'linear', "range": [-5, 100000]},
                     'yaxis': {"title": "Total deaths Linear Scale", 'type': 'linear', "range": [-5, 11000]}}]
            }
        ],
        "direction": "left",
        "pad": {"r": 10, "t": 80},
        "showactive": True,
        "type": "buttons",
        "x": 0.1,
        "xanchor": "right",
        "y": 1.7,
        "yanchor": "top",
        "font": {"color":'rgb(0, 0, 0)', "size":14}
    }
]

sliders_dict = {
    "active": 0,
    "yanchor": "top",
    "xanchor": "left",
    "currentvalue": {
        "font": {"size": 20},
        "prefix": "Year:",
        "visible": True,
        "xanchor": "right"
    },
    "transition": {"duration": 300, "easing": "cubic-in-out"},
    "pad": {"b": 10, "t": 50},
    "len": 0.9,
    "x": 0.1,
    "y": 0,
    "steps": []
}

year = 1970
for region in regions:
    dataset_by_year = RegionYearAttackDeathsDF[RegionYearAttackDeathsDF["Year"] == year]
    dataset_by_year_and_reg = dataset_by_year[
        dataset_by_year["Region"] == region]

    data_dict = {
        "x": list(dataset_by_year_and_reg["NumDeathsComul"]),
        "y": list(dataset_by_year_and_reg["NumDeathsPerYear"]),
        "mode": 'lines+markers',
        "text": list(dataset_by_year_and_reg["Year"]),
        "line": {

        },
        "name": region
    }
    fig_dict["data"].append(data_dict)

for year in years:
    frame = {"data": [], "name": str(year)}
    for region in regions:
        dataset_by_year = RegionYearAttackDeathsDF[RegionYearAttackDeathsDF["Year"] <= int(year)]
        dataset_by_year_and_reg = dataset_by_year[
            dataset_by_year["Region"] == region]

        data_dict = {
            "x": list(dataset_by_year_and_reg["NumDeathsComul"]),
            "y": list(dataset_by_year_and_reg["NumDeathsPerYear"]),
            "mode": 'lines',
            "text": list(dataset_by_year_and_reg["Year"]),
            "line": {


            },
            "name": region,
        }
        frame["data"].append(data_dict)

    fig_dict["frames"].append(frame)
    slider_step = {"args": [
        [year],
        {"frame": {"duration": 300, "redraw": True},
         "mode": "immediate",
         "transition": {"duration": 300}}
    ],
        "label": year,
        "method": "animate"}
    sliders_dict["steps"].append(slider_step)


fig_dict["layout"]["sliders"] = [sliders_dict]

DeathOverDeathFig = go.Figure(fig_dict)

DeathOverDeathFig.update_layout(
    font=dict(
        family="sans-serif",
        size=12,
        color="white"
    ),
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0,
        pad=0,
    ),

    plot_bgcolor='rgb(30,30,30)',
    paper_bgcolor='rgb(30,30,30)',
    autosize=True,
    width=725,
    height=500,
    title={
        'text': "Mortality trends by region through time",
        'y':0.97,
        'x':0,
        'xanchor': 'left',
        'yanchor': 'top'}
)

DeathsByRegion = px.line(killsByRegionDF,
                        x='Year',
                        y='NumDeaths',
                        color='Region',
                        title="Number of deaths by region through time",
                        template='plotly_dark')

DeathsByRegion.update_layout(
    coloraxis=dict(showscale=False),
    font=dict(
        family="Arial",
        size=12,
    ),
    margin=dict(
        l=50,
        r=50,
        b=50,
        t=50,
        pad=0,
    ),
    plot_bgcolor='rgb(30,30,30)',
    paper_bgcolor='rgb(30,30,30)',
    autosize=True,
    # width = 1387,
    # height=500,
    title={
        'text': "Number of deaths by region through time",
        'y': 0.97,
        'x': 0,
        'xanchor': 'left',
        'yanchor': 'top'}
)
