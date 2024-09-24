# Import required libraries
import pandas as pd
import dash
from dash import Dash, html, dash_table, dcc, Output, Input
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
import plotly.express as px
from datetime import datetime


# disaster = pd.read_csv

# Create a dash application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


# Create an app layout
app.layout = html.Div(
    [# 2 rows
        dbc.Row(# Row 1 Dashboard name and Filter
            [
                dbc.Col(  #name
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
                            dcc.Dropdown(
                                id = 'disaster-dropdown'
                            )

                        ],
                        style = {
                            
                        }                            
                    )
                    

                ])  
            ]
        ),        

        dbc.Row( # Row 2 Dashboards
            [
                dbc.Col( # Statistics: total death + total affected + total damage + country with most death + last updated
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    'Total Deaths',
                                    style = {
                                        'textAlign': 'center'
                                    }
                                ),
                                dbc.CardBody(
                                    html.Div(
                                        id = 'total-deaths'
                                ),
                                    style = {
                                        'textAlign': 'center',
                                        'font-size': '3.2vw',
                                        'align-items': 'center'
                                    }
                                )
                            ],
                            className=["h-25"]
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    'Total People Affected',
                                    style = {
                                        'textAlign': 'center'
                                    }
                                ),
                                dbc.CardBody(
                                    html.Div(
                                        id = 'total-affected'
                                ),
                                    style = {
                                        'textAlign': 'center',
                                        'font-size': '3.2vw',
                                        'align-items': 'center'
                                    }
                                )
                            ],
                            className=["h-25"]
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    'Total Damage',
                                    style = {
                                        'textAlign': 'center'
                                    }
                                ),
                                dbc.CardBody(
                                    html.Div(
                                        id = 'total-damage'
                                ),
                                    style = {
                                        'textAlign': 'center',
                                        'font-size': '3.2vw',
                                        'align-items': 'center'
                                    }
                                )
                            ],
                            className=["h-25"]
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    'Country with the most deaths',
                                    style = {
                                        'textAlign': 'center'
                                    }
                                ),
                                dbc.CardBody(
                                    html.Div(
                                        id = 'country-most-deaths'
                                ),
                                    style = {
                                        'textAlign': 'center',
                                        'font-size': '3.2vw',
                                        'align-items': 'center'
                                    }
                                )
                            ],
                            className=["h-25"]
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    'Last updated',
                                    style = {
                                        'textAlign': 'center'
                                    }
                                ),
                                dbc.CardBody(
                                    html.Div(
                                        id = 'last-updated'
                                ),
                                    style = {
                                        'textAlign': 'center',
                                        'font-size': '3.2vw',
                                        'align-items': 'center'
                                    }
                                )
                            ],
                            className=["h-25"]
                        )
                    ]
                ), 

                dbc.Col( # map total disaster & statistics:Most affected country & bar chart count of disaster by time
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader('Number of disasters'),
                                dbc.CardBody(
                                        html.Div(
                                            dcc.Graph(id='number-of-disasters')
                                        )
                                )
                            ]
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    'Most affected country',
                                    style = {
                                        'textAlign': 'center'
                                    }
                                ),
                                dbc.CardBody(
                                    html.Div(
                                        id = 'most-affected-country'
                                ),
                                    style = {
                                        'textAlign': 'center',
                                        'font-size': '3.2vw',
                                        'align-items': 'center'
                                    }
                                )
                            ],
                            className=["h-25"]
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    'Count of disasters by time',
                                    'textAlign': 'center'                                               
                                ),
                                dbc.CardBody(
                                    html.Div(
                                        dcc.Graph(id='count-disaster-by-time')
                                    )
                                )
                            ]
                        )
                    ]
                ), 


                dbc.Col( # map total damage & statistics: most damaged country  &  line chart casualty trends
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader('Total damage'),
                                dbc.CardBody(
                                        html.Div(
                                            dcc.Graph(id='total-damage')
                                        )
                                )
                            ]
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    'Most damaged country',
                                    style = {
                                        'textAlign': 'center'
                                    }
                                ),
                                dbc.CardBody(
                                    html.Div(
                                        id = 'most-damaged-country'
                                ),
                                    style = {
                                        'textAlign': 'center',
                                        'font-size': '3.2vw',
                                        'align-items': 'center'
                                    }
                                )
                        ],
                        className=["h-25"]
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader('Casualty Trend'),
                                dbc.CardBody(
                                    html.Div(
                                        dcc.Graph(id='casualty trend')
                                    )
                                )
                            ]
                        )
                    ]
                )
            ]            
        )      
    ]
)