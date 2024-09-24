# Import required libraries
import pandas as pd
import dash
from dash import Dash, html, dash_table, dcc, Output, Input
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
import plotly.express as px
from datetime import datetime

#
# disaster = pd.read_csv

# Create a dash applicatio
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


# Create an app layout
app.layout = html.Div(
    [# 2 rows
        dbc.Row(# Row 1 Dashboard name and Filter
            [
                dbc.Col(   #name
                    [
                        html.Header(
                            'Disaster Dashboard',
                        ),
                    
                    ],
                    className = ["Header"]
                ),  
                dbc.Col([ # filter 1: continent, subregion, countries
                    html.H5("Select areas"),
                    html.Div(
                        [
                            dcc.Dropdown(id = 'area-dropdown')

                        ],
                        style = {

                        }                            
                    )

                ]),  
                dbc.Col([ # filter 2: date (year - month)
                    html.H5("Select time"),
                    html.Div(
                        [
                            dcc.Dropdown(id = 'time-dropdown')

                        ],
                        style = {
                            
                        }                            
                    )

                ]),  
  
                dbc.Col([# filter 3: disaster type
                    html.H5("Select time"),
                    html.Div(
                        [
                            dcc.Dropdown(id = 'disaster-dropdown')

                        ],
                        style = {
                            
                        }                            
                    )
                    

                ])  
            ]
        ),        

        dbc.Row(
            [
                dbc.Col(), # Statistics: total death + total affected + total damage + country with most death + last updated
                dbc.Col(), # map total disaster & statistics:Most affected country & bar chart count of disaster by time
                dbc.Col(), # map total damage & statistics: most damaged country  &  line chart casualty trends
            ]),       # Row 2 Dashboards


    ]
)