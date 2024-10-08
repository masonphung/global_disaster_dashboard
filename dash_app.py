import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import webbrowser
from threading import Timer
# Load pre-defined functions that help our work
from utils import apply_filters

# Load the dataset
file_path = 'dataset/cleaned_emrat.xlsx'
data = pd.read_excel(file_path)



#### I. DATA & FUNCTIONS PREPARATION 
# Make sure datatypes are correct
data['last_update'] = pd.to_datetime(data['last_update'], errors='coerce')
# In dash, there is a problem with int64 dtype that'll not allow the dashboard to run.
# `year` is currently int64 and we work around this by converting `year` to str.
# When plotting with plotly, we'll convert it back to int later.
data['year'] = data['year'].astype(str)

# Calculate key statistics
## Total statistics
total_deaths = data['total_deaths'].sum()
total_affected = data['total_affected'].sum()
total_damage = data['total_damage'].sum()

## Most statistics
most_deaths_country = data.groupby('country')['total_deaths'].sum().idxmax()
most_affected_country = data.groupby('country')['total_affected'].sum().idxmax()
most_damaged_country = data.groupby('country')['total_damage'].sum().idxmax()

# Last update date
last_updated = data['last_update'].max()

# Prepare Year + Month filter data
data['YearMonth'] = data['year'].astype(str) + '-' + data['month'].astype(str)

# Get unique values for the dropdowns
years = sorted(data['year'].unique())
months = sorted(data['month'].unique())
continents = sorted(data['region'].unique())
subregions = sorted(data['subregion'].unique())
countries = sorted(data['country'].unique())
disaster_types = sorted(data['type'].unique())

# Get max-min year
max_year = max(years)
min_year = min(years)



#### DASH APP
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Layout of the dashboard: Consists of 2 rows.
# R1 includes the title and filter bars.
# R2 includes the dashboard cards (statistics & charts).
# There'll be more detailed layers in each of the rows.
app.layout = html.Div([
    # Row 1: Title and filter bar
    dbc.Row([
        # Col 1: Dashboard title
        dbc.Col(
            [html.H1('Global Disaster Statistics')],
            xs=12, sm=12, md=12, lg=2, xl=2
        ),
        # Col 2: Filters
        dbc.Col(
            [
            dbc.Card([
            # Must make all filters in the same row as we can't directly have a `dbc.Col` inside a `dbc.Col`
            dbc.Row([
                # Filter 1: Year and Month (Year above Month)
                dbc.Col([
                    html.Div([
                        html.Label('Year'),
                        dcc.RangeSlider(
                            # There is an developer's issue with dtype int64 (data['year'] dtype) with dcc.RangeSlider.
                            # We'll have to state the years manually in this part.
                            id='year-slider',
                            min=2000, 
                            max=2024, 
                            step=1,
                            value=[2000, 2024],
                            marks={str(i): {'label': str(i)} for i in range(2000, 2025, 4)},
                            tooltip={"placement": "bottom", "always_visible": True}
                        ),
                        html.Label('Month'),
                        dcc.Dropdown(
                            id='month-dropdown',
                            options=[{'label': str(m), 'value': str(m)} for m in months],
                            placeholder='Select Month'
                        )
                    ]),
                ], style = {'width': '40%'}),
                # Filter 2: Location (Continent, Subregion, Country in vertical stack)
                dbc.Col([
                    html.Div([
                        html.Label('Continent'),
                        dcc.Dropdown(
                            id='continent-dropdown',
                            options=[{'label': c, 'value': c} for c in continents],
                            placeholder='Select Continent'
                        ),
                        html.Label('Subregion'),
                        dcc.Dropdown(
                            id='subregion-dropdown',
                            placeholder='Select Subregion'
                        ),
                        html.Label('Country'),
                        dcc.Dropdown(
                            id='country-dropdown',
                            placeholder='Select Country'
                        )
                        ]),  
                ], style = {'width': '40%'}),
                # Filter 3: Disaster Type
                dbc.Col([
                    html.Div([
                        html.Label('Disaster Type'),
                        dcc.Checklist(
                            id='disaster-type-checkbox',
                            options = [
                                {
                                    "label": [
                                        html.Img(src="/assets/images/disaster_types/drought.jpg", 
                                                 style={'width': '50px', 'height': '35px', 'objectFit': 'cover', 'padding-left': 10}),
                                        html.Span("Drought", style={"padding-left": 10}),
                                    ],
                                    "value": "Drought",
                                },
                                {
                                    "label": [
                                        html.Img(src="/assets/images/disaster_types/earthquake.jpg", 
                                                 style={'width': '50px', 'height': '35px', 'objectFit': 'cover', 'padding-left': 10}),
                                        html.Span("Earthquake", style={"padding-left": 10}),
                                    ],
                                    "value": "Earthquake",
                                },
                                {
                                    "label": [
                                        html.Img(src="/assets/images/disaster_types/extreme_temp.jpg", 
                                                 style={'width': '50px', 'height': '35px', 'objectFit': 'cover', 'padding-left': 10}),
                                        html.Span("Extreme temperature", style={"padding-left": 10}),
                                    ],
                                    "value": "Extreme temperature",
                                },
                                {
                                    "label": [
                                        html.Img(src="/assets/images/disaster_types/flood.jpg", 
                                                 style={'width': '50px', 'height': '35px', 'objectFit': 'cover', 'padding-left': 10}),
                                        html.Span("Flood", style={"padding-left": 10}),
                                    ],
                                    "value": "Flood",
                                },
                                {
                                    "label": [
                                        html.Img(src="/assets/images/disaster_types/mass_movement.jpg", 
                                                 style={'width': '50px', 'height': '35px', 'objectFit': 'cover', 'padding-left': 10}),
                                        html.Span("Mass movement", style={"padding-left": 10}),
                                    ],
                                    "value": "Mass movement",
                                },
                                {
                                    "label": [
                                        html.Img(src="/assets/images/disaster_types/storm.jpeg",
                                                 style={'width': '50px', 'height': '35px', 'objectFit': 'cover', 'padding-left': 10}),
                                        html.Span("Storm", style={"padding-left": 10}),
                                    ],
                                    "value": "Storm",
                                },
                                {
                                    "label": [
                                        html.Img(src="/assets/images/disaster_types/volcanic.jpg", 
                                                 style={'width': '50px', 'height': '35px', 'objectFit': 'cover', 'padding-left': 10}),
                                        html.Span("Volcanic activity", style={"padding-left": 10}),
                                    ],
                                    "value": "Volcanic activity",
                                },
                                {
                                    "label": [
                                        html.Img(src="/assets/images/disaster_types/wildfire.jpg",
                                                 style={'width': '50px', 'height': '35px', 'objectFit': 'cover', 'padding-left': 10}),
                                        html.Span("Wildfire", style={"padding-left": 10}),
                                    ],
                                    "value": "Wildfire",
                                }
                            ],
                            value=disaster_types,
                            inline = True,
                            style={
                                'display': 'flex', 'flexDirection': 'row', 
                                'flexWrap': 'wrap', 'display':'grid',
                                'gridTemplateColumns': 'repeat(2, 1fr)', 'gap': '10px'}
                        )
                    ])
                ], style = {'width': '20%'})
            ])])],xs=12, sm=12, md=12, lg=10, xl=10
        )
    ],style={'display': 'flex', 'flexDirection': 'row', 'margin': '5px'}),
    
    # Row 2: Statistics cards and graphs                
    dbc.Row([
        # Col 1: Statistics
        dbc.Col(
            [
                # Card 1: Total deaths
                dbc.Card([
                    dbc.CardHeader(
                        'Total Casualty', 
                        style={'textAlign': 'center'}
                    ),
                    dbc.CardBody(
                        html.H3(id='total-deaths-card'),
                        style={'textAlign': 'center', 'alignItems': 'center'}
                    )
                ],className=["h-25"]),
                # Card 2: Total Affected
                dbc.Card([
                    dbc.CardHeader(
                        'Total People Affected', 
                        style={'textAlign': 'center'}
                    ),
                    dbc.CardBody(
                        html.H3(id='total-affected-card'),
                        style={'textAlign': 'center', 'alignItems': 'center'}
                    )
                ],className=["h-25"]),
                # Card 3: Total Damage
                dbc.Card([
                    dbc.CardHeader(
                        'Total Damage in USD', 
                        style={'textAlign': 'center'}
                    ),
                    dbc.CardBody(
                        html.H3(id='total-damage-card'),
                        style={'textAlign': 'center', 'alignItems': 'center'}
                    )
                ],className=["h-25"]),
                # Card 4: Most affected country
                dbc.Card([
                    dbc.CardHeader(
                        'Most Affected Country', 
                        style={'textAlign': 'center'}
                    ),
                    dbc.CardBody(
                        html.H3(id='most-affected-country-card'),
                        style={'textAlign': 'center', 'alignItems': 'center'}
                    )
                ],className=["h-25"]),
                # Card 5: Most damaged country
                dbc.Card([
                    dbc.CardHeader(
                        'Most Damaged Country', 
                        style={'textAlign': 'center'}
                    ),
                    dbc.CardBody(
                        html.H3(id='most-damaged-country-card'),
                        style={'textAlign': 'center', 'alignItems': 'center'}
                    )
                ],className=["h-25"]),
                # Card 6: Country with most deaths
                dbc.Card([
                    dbc.CardHeader(
                        'Country with Highest Casualty', 
                        style={'textAlign': 'center'}
                    ),
                    dbc.CardBody(
                        html.H3(id='most-deaths-country-card'),
                        style={'textAlign': 'center', 'alignItems': 'center'}
                    )
                ],className=["h-25"]),
                # Card 7: Data last updated date
                dbc.Card([
                    dbc.CardHeader(
                        'Last Updated', 
                        style={'textAlign': 'center'}
                    ),
                    dbc.CardBody(
                        html.H3(id='last-updated-card', children=last_updated.strftime('%Y-%m-%d')),
                        style={'textAlign': 'center', 'alignItems': 'center'}
                    )
                ],className=["h-25"]),
            ],
            className = [
                'd-flex',
                'justify-content-between',
                'flex-column'
            ],
            xs=12, sm=12, md=2, lg=2, xl=2),
        
        # Col 2: Map and chart A
        dbc.Col(
            [
                # Map-A
                dbc.Card([
                    dbc.CardHeader('Total Damage by Country'),
                    dbc.CardBody(
                        html.Div(
                            dcc.Graph(id='damage-map', style={'height': '500px'})
                        )
                    )
                ]),
                # Chart-A
                dbc.Card([
                    dbc.CardHeader('Total number of disaster by year and type'),
                    dbc.CardBody(
                        html.Div(
                            dcc.Graph(id='stacked-bar-chart', style={'height': '500px'})
                        )
                    )
                ]),
            ], xs=12, sm=12, md=12, lg=5, xl=5
        ),
        # Col 3: Map and chart B
        dbc.Col(
            [
                # Map-B
                dbc.Card([
                    dbc.CardHeader('Total amount of disaster'),
                    dbc.CardBody(
                        html.Div(
                            dcc.Graph(id='disaster-count-map', style={'height': '500px'})
                        )
                    )
                ]),
                # Chart-B
                dbc.Card([
                    dbc.CardHeader('Casualty trends by year'),
                    dbc.CardBody(
                        html.Div(
                            dcc.Graph(id='casualty-trend', style={'height': '500px'})
                        )
                    )
                ])   
            ], xs=12, sm=12, md=12, lg=5, xl=5
        ),
    ],style={'display': 'flex', 'flexDirection': 'row', 'margin': '5px'}),
])

# Filter A: Update the subregion dropdown based on selected continent
@app.callback(
    Output('subregion-dropdown', 'options'),
    Input('continent-dropdown', 'value')
)
def update_subregions(selected_continent):
    if selected_continent:
        filtered_subregions = data[data['region'] == selected_continent]['subregion'].unique()
        return [{'label': s, 'value': s} for s in filtered_subregions]
    return []

# Filter B: Update the country dropdown based on selected subregion
@app.callback(
    Output('country-dropdown', 'options'),
    Input('subregion-dropdown', 'value')
)
def update_countries(selected_subregion):
    if selected_subregion:
        filtered_countries = data[data['subregion'] == selected_subregion]['country'].unique()
        return [{'label': c, 'value': c} for c in filtered_countries]
    return []

# Stats-A: Total deaths, total affected, and total damage cards
@app.callback(
    [Output('total-deaths-card', 'children'),
     Output('total-affected-card', 'children'),
     Output('total-damage-card', 'children')],
    [Input('continent-dropdown', 'value'),
     Input('subregion-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('year-slider', 'value'),
     Input('month-dropdown', 'value'),
     Input('disaster-type-checkbox', 'value')]
)
def update_stat_cards(selected_continent, selected_subregion, selected_country, selected_year, selected_month, selected_disaster_type):
    # Use the helper function to filter data
    filtered_data = apply_filters(data, selected_continent, selected_subregion, selected_country, selected_year, selected_month, selected_disaster_type)

    # Calculate totals for the filtered data
    total_deaths = filtered_data['total_deaths'].sum().astype(int)
    total_affected = filtered_data['total_affected'].sum().astype(int)
    total_damage = filtered_data['total_damage'].sum().astype(int)

    # Format the values with commas for better readability
    return (f"{total_deaths:,}", f"{total_affected:,}", f"{total_damage:,}")

# Stats-B: Most Affected, Most Damaged, Country with Most Deaths, Last Updated
@app.callback(
    [Output('most-affected-country-card', 'children'),
     Output('most-damaged-country-card', 'children'),
     Output('most-deaths-country-card', 'children'),
     Output('last-updated-card', 'children')],
    [Input('continent-dropdown', 'value'),
     Input('subregion-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('year-slider', 'value'),
     Input('month-dropdown', 'value'),
     Input('disaster-type-checkbox', 'value')]
)
def update_remaining_cards(selected_continent, selected_subregion, selected_country, selected_year, selected_month, selected_disaster_type):
    # Use the helper function to filter data
    filtered_data = apply_filters(data, selected_continent, selected_subregion, selected_country, selected_year, selected_month, selected_disaster_type)

    # Get country with most affected
    most_affected_country = filtered_data.groupby('country')['total_affected'].sum().idxmax() if not filtered_data.empty else 'N/A'
    
    # Get country with most damage
    most_damaged_country = filtered_data.groupby('country')['total_damage'].sum().idxmax() if not filtered_data.empty else 'N/A'

    # Get country with most deaths
    most_deaths_country = filtered_data.groupby('country')['total_deaths'].sum().idxmax() if not filtered_data.empty else 'N/A'

    # Get last updated date
    last_updated = filtered_data['last_update'].max() if not filtered_data.empty else 'N/A'

    # Return values for the cards
    return (most_affected_country, most_damaged_country, most_deaths_country, last_updated.strftime('%Y-%m-%d') if last_updated != 'N/A' else last_updated)

# Map-A: Total damage choropleth map based on filters
@app.callback(
    Output('damage-map', 'figure'),
    [Input('continent-dropdown', 'value'),
     Input('subregion-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('year-slider', 'value'),
     Input('month-dropdown', 'value'),
     Input('disaster-type-checkbox', 'value')]
)
def plot_map_damage_heat(selected_continent, selected_subregion, selected_country, selected_year, selected_month, selected_disaster_type):
    # Use the helper function to filter data
    filtered_data = apply_filters(data, selected_continent, selected_subregion, selected_country, selected_year, selected_month, selected_disaster_type)

    # Create choropleth map for total damage
    fig = px.choropleth(
        data_frame=filtered_data,
        locations='country',
        locationmode='country names',
        color='total_damage',
        hover_name='country',
        color_continuous_scale='Reds',
        range_color = [0, 10000000],
        labels={'total_damage': 'Damage (USD)'}
    )
    fig.update_geos(
        showcoastlines=True,
        fitbounds = 'locations',
        coastlinecolor="Black",
        showland=True, landcolor="lightgray", visible=False
    )
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        legend=dict(
            orientation='h',
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig

# Map-B: The disaster count choropleth map based on filters
@app.callback(
    Output('disaster-count-map', 'figure'),
    [Input('continent-dropdown', 'value'),
     Input('subregion-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('year-slider', 'value'),
     Input('month-dropdown', 'value'),
     Input('disaster-type-checkbox', 'value')]
)
def plot_map_disaster_heat(selected_continent, selected_subregion, selected_country, selected_year, selected_month, selected_disaster_type):
    # Use the helper function to filter data
    filtered_data = apply_filters(data, selected_continent, selected_subregion, selected_country, selected_year, selected_month, selected_disaster_type)

    # Create choropleth map for total number of disasters
    disaster_count_filtered = filtered_data.groupby('country')['id'].count().reset_index()
    disaster_count_filtered.columns = ['country', 'total_disasters']

    fig = px.choropleth(
        data_frame=disaster_count_filtered,
        locations='country',
        locationmode='country names',
        color='total_disasters',
        hover_name='country',
        color_continuous_scale='Reds',
        labels={'total_disasters': 'Total Number of Disasters'}
    )

    fig.update_geos(
        showcoastlines=True,
        fitbounds = 'locations',
        coastlinecolor="Black",
        showland=True, landcolor="lightgray", visible=False
    )
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    return fig

# Chart-A: The stacked bar chart based on filters
@app.callback(
    Output('stacked-bar-chart', 'figure'),
    [Input('continent-dropdown', 'value'),
     Input('subregion-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('year-slider', 'value'),
     Input('month-dropdown', 'value'),
     Input('disaster-type-checkbox', 'value')]
)
def plot_bar_total_disaster(selected_continent, selected_subregion, selected_country, selected_year, selected_month, selected_disaster_type):
    # Use the helper function to filter data
    filtered_data = apply_filters(data, selected_continent, selected_subregion, selected_country, selected_year, selected_month, selected_disaster_type)

    # Group by year and type for the filtered data
    disasters_type_and_year = filtered_data.groupby(['year', 'type']).size().reset_index(name='total_disasters')

    # Convert 'year' to int
    disasters_type_and_year['year'] = disasters_type_and_year['year'].astype(int)
    
    # Map the colors based on the disaster type
    disaster_colors = {
        'Drought': 'gold', 'Earthquake': 'gray', 'Extreme temperature': 'red', 'Flood': 'blue',
        'Mass movement': 'green', 'Storm': 'lightblue', 'Volcanic activity': 'purple', 'Wildfire': 'cyan'}
    
    # Create stacked bar chart for total disasters by type and year
    fig = px.bar(
        disasters_type_and_year,
        x='year',
        y='total_disasters',
        color='type',
        color_discrete_map = disaster_colors,
        labels={'total_disasters': 'Total Disasters'}
    )
    fig.update_layout(
        xaxis = dict(
            title = 'Year',
            tickvals = [i for i in range(2000, 2025, 4)],
        ),
        yaxis_title='Total Disasters',
        plot_bgcolor='white',
        margin=dict(l=40, r=40, t=40, b=40),
        legend=dict(
            orientation='h',
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig

# Chart-B: Total death by year
@app.callback(
    Output('casualty-trend', 'figure'),
    [Input('continent-dropdown', 'value'),
     Input('subregion-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('year-slider', 'value'),
     Input('month-dropdown', 'value'),
     Input('disaster-type-checkbox', 'value')]
)
def plot_line_casualty_trend(selected_continent, selected_subregion, selected_country, selected_year, selected_month, selected_disaster_type):
    # Use the helper function to filter data
    filtered_data = apply_filters(data, selected_continent, selected_subregion, selected_country, selected_year, selected_month, selected_disaster_type)

    # Group by year and calculate total deaths
    deaths_by_year = filtered_data.groupby('year')['total_deaths'].sum().reset_index()
    
    # Convert 'year' to int
    deaths_by_year['year'] = deaths_by_year['year'].astype(int)

    # Create the line chart for Casualty Trend
    fig = px.line(
        deaths_by_year,
        x='year',
        y='total_deaths',
        labels={'total_deaths': 'Total Deaths', 'year': 'Year'},
    )

    # Customize the layout of the line chart
    fig.update_layout(
        xaxis = dict(
            title = 'Year',
            tickvals = [i for i in range(2000, 2025, 4)],
        ),
        yaxis_title='Total Deaths',
        plot_bgcolor='white',
        hovermode='x unified',
        margin=dict(l=40, r=40, t=40, b=40),
        legend=dict(
            orientation='h',
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig

# Run the app
# def open_browser():
    # webbrowser.open_new("http://127.0.0.1:8050/")

# Only open the browser if the script is run directly
if __name__ == "__main__":
    # Start the Dash app and open the browser automatically after a slight delay
    # Timer(1, open_browser).start()
    app.run_server(debug=True)