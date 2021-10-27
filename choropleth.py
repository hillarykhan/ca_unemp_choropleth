from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import geopandas as gpd
import plotly.express as px
import json
import requests


from app import app
from app import server


try:
    # print("BEFORE")
    unemp_request = requests.get('https://ca-county-unemp.herokuapp.com/unemployment', timeout=3).json()
    # print("AFTER")
    # print(unemp_request)
    df = pd.DataFrame(unemp_request)

except Exception as e:
    print(e)

ca_counties = json.load(open('/Users/hillarykhan/Desktop/apca_choro/data/ca-county-boundaries.geojson', 'r'))

for feature in ca_counties['features']:
    feature['id'] = feature['properties']['geoid']

geo_df = gpd.GeoDataFrame.from_features(
    ca_counties["features"])

# print("geo_df: ", geo_df.head())
# DATA WRANGLING ENDS

# APP LAYOUT STARTS
app.layout = html.Div([
    html.H2("California Unemployment Rates by County", style={'text-align': 'left'}),

    dcc.Dropdown(id="slct_year",
    options=[
        {"label": "2001", "value": 2001},
        {"label": "2002", "value": 2002},
        {"label": "2003", "value": 2003},
        {"label": "2004", "value": 2004},
        {"label": "2005", "value": 2005},
        {"label": "2006", "value": 2006},
        {"label": "2007", "value": 2007},
        {"label": "2008", "value": 2008},
        {"label": "2009", "value": 2009},
        {"label": "2010", "value": 2010},
        {"label": "2011", "value": 2011},
        {"label": "2012", "value": 2012},
        {"label": "2013", "value": 2013},
        {"label": "2014", "value": 2014},
        {"label": "2015", "value": 2015},
        {"label": "2016", "value": 2016},
        {"label": "2017", "value": 2017},
        {"label": "2018", "value": 2018},
        {"label": "2019", "value": 2019},
        {"label": "2020", "value": 2020}],
    multi=False,
    value=2016,
    style={'width': "30%"}
    ),

    html.Br(),
    html.Br(),
    html.Br(),

    dcc.Graph(id='my_unemp_map', figure={})

])
# APP LAYOUT ENDS


# CALLBACK STARTS

@app.callback(
    Output(component_id='my_unemp_map', component_property='figure'),
    [Input(component_id='slct_year', component_property='value')]
)

def update_graph(option_slctd):
    # print(option_slctd)
    # print(type(option_slctd))

    dff = df.copy()
    # print("dff: ", dff.head())
    dff = dff[dff['year'] == option_slctd]

    # print("dff with year chosen", dff.head())

    fig = px.choropleth(
        dff,
        locations='geoid',
        geojson=ca_counties,
        color='rate',
        hover_name='county',
        hover_data=['rate'])
    fig.update_geos(fitbounds='locations', visible=False)
    fig.update_layout(height=600, margin={"r":0,"t":0,"l":0,"b":0})
    return fig
# CALLBACK ENDS

if __name__ == '__main__':
    app.run_server(debug=True)