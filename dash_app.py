import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go  
import webbrowser
from threading import Timer
# Load pre-defined functions that help our work
from utils import *

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
app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5'}]
)
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
            className = ['col', 'dflex'],
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
                            tooltip={"placement": "bottom", "always_visible": True},
                            #className="form-range"
                        ),
                        html.Label('Month'),
                        dcc.Dropdown(
                            id='month-dropdown',
                            options=[
                                {'label': 'January', 'value': 1},
                                {'label': 'February', 'value': 2},
                                {'label': 'March', 'value': 3},
                                {'label': 'April', 'value': 4},
                                {'label': 'May', 'value': 5},
                                {'label': 'June', 'value': 6},
                                {'label': 'July', 'value': 7},
                                {'label': 'August', 'value': 8},
                                {'label': 'September', 'value': 9},
                                {'label': 'October', 'value': 10},
                                {'label': 'November', 'value': 11},
                                {'label': 'December', 'value': 12}],
                            placeholder='Select Month'
                        ),
                        dbc.Button("Reset Filter", id="clear-filter", style={'padding-top': 10})
                    ]),
                ], className = ['vw-40'], 
                xs=12, sm=12, md=12, lg=4, xl=4),
                # Filter 2: Location (Continent, Subregion, Country in vertical stack)
                dbc.Col([
                    html.Div([
                        html.Label('Continent'),
                        dcc.Dropdown(
                            id='continent-dropdown',
                            options=[{'label': c, 'value': c} for c in continents],
                            placeholder='Select Continent',
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
                ], className = ['vw-40'], 
                xs=12, sm=12, md=12, lg=3, xl=4),
                # Filter 3: Disaster Type
                dbc.Col([
                    html.Div([
                        html.Label('Disaster Type'),
                        dcc.Checklist(
                            className="form-check",
                            id='disaster-type-checkbox',
                            options = [
                                {
                                    "label": [
                                        html.Img(src="/assets/images/disaster_types/drought.jpg", 
                                                 style={'width': '60px', 'height': '35px', 'objectFit': 'cover', 'padding-left': 10}),
                                        html.Span("Drought", style={"padding-left": 10}),
                                    ],
                                    "value": "Drought",
                                },
                                {
                                    "label": [
                                        html.Img(src="/assets/images/disaster_types/earthquake.jpg", 
                                                 style={'width': '60px', 'height': '35px', 'objectFit': 'cover', 'padding-left': 10}),
                                        html.Span("Earthquake", style={"padding-left": 10}),
                                    ],
                                    "value": "Earthquake",
                                },
                                {
                                    "label": [
                                        html.Img(src="/assets/images/disaster_types/extreme_temp.jpg", 
                                                 style={'width': '60px', 'height': '35px', 'objectFit': 'cover', 'padding-left': 10}),
                                        html.Span("Extreme temp", style={"padding-left": 10}),
                                    ],
                                    "value": "Extreme temperature",
                                },
                                {
                                    "label": [
                                        html.Img(src="/assets/images/disaster_types/flood.jpg", 
                                                 style={'width': '60px', 'height': '35px', 'objectFit': 'cover', 'padding-left': 10}),
                                        html.Span("Flood", style={"padding-left": 10}),
                                    ],
                                    "value": "Flood",
                                },
                                {
                                    "label": [
                                        html.Img(src="/assets/images/disaster_types/mass_movement.jpg", 
                                                 style={'width': '60px', 'height': '35px', 'objectFit': 'cover', 'padding-left': 10}),
                                        html.Span("Mass movement", style={"padding-left": 10}),
                                    ],
                                    "value": "Mass movement",
                                },
                                {
                                    "label": [
                                        html.Img(src="/assets/images/disaster_types/storm.jpeg",
                                                 style={'width': '60px', 'height': '35px', 'objectFit': 'cover', 'padding-left': 10}),
                                        html.Span("Storm", style={"padding-left": 10}),
                                    ],
                                    "value": "Storm",
                                },
                                {
                                    "label": [
                                        html.Img(src="/assets/images/disaster_types/volcanic.jpg", 
                                                 style={'width': '60px', 'height': '35px', 'objectFit': 'cover', 'padding-left': 10}),
                                        html.Span("Volcanic activity", style={"padding-left": 10}),
                                    ],
                                    "value": "Volcanic activity",
                                },
                                {
                                    "label": [
                                        html.Img(src="/assets/images/disaster_types/wildfire.jpg",
                                                 style={'width': '60px', 'height': '35px', 'objectFit': 'cover', 'padding-left': 10}),
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
                                'gridTemplateColumns': 'repeat(2, 1fr)', 'gap': '5px'}
                        )
                    ])
                ], className = ['vw-20'], 
                xs=12, sm=12, md=12, lg=5, xl=4)
            ])],style = {'padding-bottom': '1vh'})], 
            className = ['col', 'dflex'], 
            xs=12, sm=12, md=12, lg=10, xl=10
        )
    ], className=['row', 'vh-25']),
    
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
                        html.Div([
                            html.H3(id='total-deaths-card', style={'textAlign': 'center', 'alignItems': 'center'}),  # Output value
                            html.P("deaths", style={'textAlign': 'center', 'marginTop': '10px'})  # Text below the output
                        ])
                    )
                ],className=['card']),
                # Card 2: Total Affected
                dbc.Card([
                    dbc.CardHeader(
                        'Total People Affected', 
                        style={'textAlign': 'center'}
                    ),
                    dbc.CardBody(
                        html.Div([
                            html.H3(id='total-affected-card', style={'textAlign': 'center', 'alignItems': 'center'}),  # Output value
                            html.P("people", style={'textAlign': 'center', 'marginTop': '10px'})  # Text below the output
                        ])
                    )
                ],className=['card']),
                # Card 3: Total Damage
                dbc.Card([
                    dbc.CardHeader(
                        'Total Damage', 
                        style={'textAlign': 'center'}
                    ),
                    dbc.CardBody(
                        html.Div([
                            html.H3(id='total-damage-card', style={'textAlign': 'center', 'alignItems': 'center'}),  # Output value
                            html.P("US$", style={'textAlign': 'center', 'marginTop': '10px'})  # Text below the output
                        ])
                    )
                ],className=['card']),
                # Card 4: Country with most deaths
                dbc.Card([
                    dbc.CardHeader(
                        'Country with the Highest Casualty', 
                        style={'textAlign': 'center'}
                    ),
                    dbc.CardBody(
                        html.H3(id='most-deaths-country-card'),
                        style={'textAlign': 'center', 'alignItems': 'center'}
                    )
                ],className=['card']),
                # Card 5: Most affected country
                dbc.Card([
                    dbc.CardHeader(
                        'Country with the Most People Affected', 
                        style={'textAlign': 'center'}
                    ),
                    dbc.CardBody(
                        html.H3(id='most-affected-country-card'),
                        style={'textAlign': 'center', 'alignItems': 'center'}
                    )
                ],className=['card']),
                # Card 6: Most damaged country
                dbc.Card([
                    dbc.CardHeader(
                        'Country with the Highest Damage', 
                        style={'textAlign': 'center'}
                    ),
                    dbc.CardBody(
                        html.H3(id='most-damaged-country-card'),
                        style={'textAlign': 'center', 'alignItems': 'center'}
                    )
                ],className=['card']),
                # Card 7: Data last updated date
                dbc.Card([
                    dbc.CardHeader(
                        'Data Last Update', 
                        style={'textAlign': 'center'}
                    ),
                    dbc.CardBody(
                        html.H3(id='last-updated-card', children=last_updated.strftime('%Y-%m-%d')),
                        className = ['card-body']
                    )
                ],className=['card']),
            ],
            className=[
                'col',
                'd-flex',
                'justify-content-between',
                'flex-column'
            ],
            xs=12, sm=12, md=12, lg=12, xl=2),
        # Col 2: Map and chart A
        dbc.Col(
            [
                create_plot_card('damage-map', 'damage-map-header'),
                create_plot_card('disaster-count-map', 'disaster-count-map-header')
            ], 
            className=[
                'col',
                'd-flex',
                'justify-content-between',
                'flex-column'
            ],  
            xs=12, sm=12, md=12, lg=12, xl=5
        ),
        # Col 3: Map and chart B
        dbc.Col(
            [
                create_plot_card('stacked-bar-chart', 'stacked-bar-chart-header'),
                create_plot_card('casualty-trend', 'casualty-trend-header')
            ], 
            className=[
                'col',
                'd-flex',
                'justify-content-between',
                'flex-column'
            ],  
            xs=12, sm=12, md=12, lg=12, xl=5
        ),
    ], className = ['row', 'vh-75']),
])

# Filter B1: Update the subregion dropdown based on selected continent
@app.callback(
    Output('subregion-dropdown', 'options'),
    Input('continent-dropdown', 'value')
)
def update_subregions(selected_continent):
    if selected_continent:
        filtered_subregions = data[data['region'] == selected_continent]['subregion'].unique()
        return [{'label': s, 'value': s} for s in filtered_subregions]
    return []

# Filter B2: Update the country dropdown based on selected subregion
@app.callback(
    Output('country-dropdown', 'options'),
    Input('subregion-dropdown', 'value')
)
def update_countries(selected_subregion):
    if selected_subregion:
        filtered_countries = data[data['subregion'] == selected_subregion]['country'].unique()
        return [{'label': c, 'value': c} for c in filtered_countries]
    return []

# Reset filter button
@app.callback(
    [Output('continent-dropdown', 'value'),
    Output('subregion-dropdown', 'value'),
    Output('country-dropdown', 'value'),
    Output('year-slider', 'value'),
    Output('month-dropdown', 'value'),
    Output('disaster-type-checkbox', 'value')],
    [Input("clear-filter", "n_clicks")],
    prevent_initial_call=True
)
def reset_filters(n_clicks):
    return (
        None,  # Reset continent dropdown to None or default value
        None,  # Reset subregion dropdown to None or default value
        None,  # Reset country dropdown to None or default value
        [2000, 2024],  # Reset year slider to the default range
        None,          # Reset month dropdown to None or default value
        disaster_types # Reset disaster type checklist to the original list
    )



# Stats: Update all the statistics cards
@app.callback(
    [Output('total-deaths-card', 'children'),
     Output('total-affected-card', 'children'),
     Output('total-damage-card', 'children'),
     Output('most-deaths-country-card', 'children'),
     Output('most-affected-country-card', 'children'),
     Output('most-damaged-country-card', 'children'),
     Output('last-updated-card', 'children')],
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

    # Get country with most affected
    most_affected_country = filtered_data.groupby('country')['total_affected'].sum().idxmax() if not filtered_data.empty else 'N/A'
    
    # Get country with most damage
    most_damaged_country = filtered_data.groupby('country')['total_damage'].sum().idxmax() if not filtered_data.empty else 'N/A'

    # Get country with most deaths
    most_deaths_country = filtered_data.groupby('country')['total_deaths'].sum().idxmax() if not filtered_data.empty else 'N/A'

    # Get last updated date
    last_updated = filtered_data['last_update'].max() if not filtered_data.empty else 'N/A'

    # Format the values with commas for better readability
    return (f"{total_deaths:,}", f"{total_affected:,}", f"{total_damage:,}",
            most_deaths_country, most_affected_country, most_damaged_country, last_updated.strftime('%Y-%m-%d') if last_updated != 'N/A' else last_updated)

# Map-A: Total damage choropleth map based on filters
@app.callback(
    [Output('damage-map', 'figure'),
     Output('damage-map-header', 'children')],
    [Input('continent-dropdown', 'value'),
     Input('subregion-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('year-slider', 'value'),
     Input('month-dropdown', 'value'),
     Input('disaster-type-checkbox', 'value')]
)

def plot_map_damage_heat(selected_continent, selected_subregion, selected_country, selected_year, selected_month, selected_disaster_type):
# Update the plot card header name
    base_header = "Total damage inflicted by "
    card_header_text = generate_header(base_header, selected_disaster_type, selected_year, selected_month)

    # Use the helper function to filter data
    filtered_data = apply_filters(data, selected_continent, selected_subregion, selected_country, selected_year, selected_month, selected_disaster_type)

    # Use the pre-existing column 'total_damage_total_country' for total damage per country
    filtered_data = filtered_data[['country', 'total_damage_total_country']].drop_duplicates()

    # Categorize total damage into 5 categories using 'total_damage_total_country'
    bins = [-1, 1_000_000, 10_000_000, 100_000_000, 500_000_000, float('inf')]
    labels = ['0 - 1M', '1M - 10M', '10M - 100M', '100M - 500M', '> 500M']

    # Add the categorization column based on 'total_damage_total_country'
    filtered_data['damage_category'] = pd.cut(
        filtered_data['total_damage_total_country'], 
        bins=bins, 
        labels=labels,
        ordered=True
    )

    # Ensure 'damage_category' is a categorical type with the specified order
    filtered_data['damage_category'] = pd.Categorical(
        filtered_data['damage_category'],
        categories=labels,
        ordered=True
    )

    # Identify missing categories
    existing_categories = filtered_data['damage_category'].dropna().unique()
    missing_categories = set(labels) - set(existing_categories)

    if missing_categories:
        # Create dummy data for missing categories
        missing_df = pd.DataFrame({
            'country': [None]*len(missing_categories),
            'total_damage_total_country': [0]*len(missing_categories),
            'damage_category': pd.Categorical(list(missing_categories), categories=labels, ordered=True)
        })
        filtered_data = pd.concat([filtered_data, missing_df], ignore_index=True)

    # Sort the DataFrame by 'damage_category' to ensure correct plotting order
    filtered_data.sort_values('damage_category', inplace=True)

    # Explicit color mapping to ensure the correct order of categories
    category_colors = {
        '0 - 1M': '#fee5d9',
        '1M - 10M': '#fcae91',
        '10M - 100M': '#fb6a4a',
        '100M - 500M': '#de2d26',
        '> 500M': '#a50f15'
    }

    # Create choropleth map for total damage categorized
    fig = px.choropleth(
        filtered_data,
        locations='country',
        locationmode='country names',
        color='damage_category',  # Use the 'damage_category' column for color
        hover_name='country',
        hover_data={'total_damage_total_country': True, 'damage_category': False},  # Show total damage in hover but not the category
        color_discrete_map=category_colors,  # Use explicit color mapping
        labels={'damage_category': 'Damage Category', 'total_damage_total_country': 'Total Damage (USD)'},
        category_orders={'damage_category': labels}  # Force the correct legend order
    )

    # Customize the map's appearance
    fig.update_geos(
        showcoastlines=True,
        fitbounds='locations',
        coastlinecolor="Black",
        showland=True, landcolor="lightgray", visible=False
    )

    fig.update_layout(
        margin={"r":0, "t":0, "l":0, "b":0},
        legend=dict(
            orientation='h',
            yanchor="bottom",
            y=-0.1,
            xanchor="center",
            x=0.5,
            font=dict(size=9),
            title=dict(text="Total Damage (USD)", side="top")  # Add this line for the legend title
        )
    )

    return fig, card_header_text



# Map-B: The disaster count choropleth map based on filters
@app.callback(
    [Output('disaster-count-map', 'figure'),
    Output('disaster-count-map-header', 'children')],
    [Input('continent-dropdown', 'value'),
     Input('subregion-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('year-slider', 'value'),
     Input('month-dropdown', 'value'),
     Input('disaster-type-checkbox', 'value')]
)


def plot_map_disaster_count_bubble(selected_continent, selected_subregion, selected_country, selected_year, selected_month, selected_disaster_type):
    # Update the plot card header name
    base_header = "Total number of "
    card_header_text = generate_header(
        base_header, selected_disaster_type, selected_year, selected_month
    )
    
    # Use the helper function to filter data
    filtered_data = apply_filters(
        data, selected_continent, selected_subregion, selected_country, 
        selected_year, selected_month, selected_disaster_type
    )

    # Aggregate the number of disasters per country
    disaster_count_filtered = (
        filtered_data.groupby('country')['id'].count().reset_index()
    )
    disaster_count_filtered.columns = ['country', 'total_disasters']

    # Categorize the total number of disasters into 3 categories
    bins = [-1, 150, 300, 450, 600, float('inf')]
    labels = ['0 - 150', '150 - 300', '300 - 450', '450 - 600', '> 600']
    
    # Add the categorization column based on 'total_disasters'
    disaster_count_filtered['disaster_category'] = pd.cut(
        disaster_count_filtered['total_disasters'], 
        bins=bins, 
        labels=labels, 
        ordered=True
    )

    # Ensure 'disaster_category' is a categorical type with the specified order
    disaster_count_filtered['disaster_category'] = pd.Categorical(
        disaster_count_filtered['disaster_category'],
        categories=labels,
        ordered=True
    )

    # Identify missing categories
    existing_categories = disaster_count_filtered['disaster_category'].dropna().unique()
    missing_categories = set(labels) - set(existing_categories)

    if missing_categories:
        # Use a valid country that is unlikely to overlap with existing data
        dummy_country = 'Antarctica'  # Assuming 'Antarctica' is recognized by Plotly

        # Create dummy data for missing categories
        missing_df = pd.DataFrame({
            'country': [dummy_country]*len(missing_categories),
            'total_disasters': [1]*len(missing_categories),  # Small value to avoid zero-size markers
            'disaster_category': pd.Categorical(
                list(missing_categories), categories=labels, ordered=True
            ),
            'is_dummy': [True]*len(missing_categories)
        })
        disaster_count_filtered['is_dummy'] = False  # Add a flag for existing data
        disaster_count_filtered = pd.concat(
            [disaster_count_filtered, missing_df], ignore_index=True
        )
    else:
        disaster_count_filtered['is_dummy'] = False

    # Sort the DataFrame by the disaster category to ensure plotting order
    disaster_count_filtered.sort_values('disaster_category', inplace=True)

    # **Explicit color mapping to ensure the correct order of categories**
    category_colors = {
        '0 - 150': '#fee5d9',    # Light color for low disaster counts
        '150 - 300': '#fcae91',  # Slightly darker color for mid-low counts
        '300 - 450': '#fb6a4a',  # Darker color for mid-high counts
        '450 - 600': '#de2d26',  # Even darker color for higher counts
        '> 600': '#a50f15'       # Darkest color for the highest count
    }

    # Create scatter_geo map for total number of disasters categorized
    fig = px.scatter_geo(
        disaster_count_filtered,
        locations='country',
        locationmode='country names',
        color='disaster_category',
        hover_name='country',
        size='total_disasters',
        hover_data={'total_disasters': True, 'disaster_category': False},
        color_discrete_map=category_colors,
        labels={
            'disaster_category': 'Disaster Category',
            'total_disasters': 'Total Number of Disasters'
        },
        category_orders={'disaster_category': labels}
    )

    # Update marker opacity to hide dummy data points
    fig.update_traces(
        selector=dict(mode='markers'),
        marker=dict(
            opacity=disaster_count_filtered['is_dummy'].map({True: 0, False: 0.6}).tolist()
        )
    )

    # Customize the map's appearance
    fig.update_geos(
        showcoastlines=True,
        fitbounds='locations',
        coastlinecolor="Black",
        showland=True,
        landcolor="lightgray",
        visible=False
    )
    
    # Adjust the layout and margins, ensuring all categories are visible and correctly ordered
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        legend=dict(
            orientation='h',
            yanchor="top",
            y=-0.1,
            xanchor="center",
            x=0.5,
            traceorder="normal",
            itemsizing="constant",
            font=dict(size=9),
            title=dict(text="Number of Disasters", side="top")
        )
    )

    return fig, card_header_text


# Chart-A: The stacked bar chart based on filters
@app.callback(
    [Output('stacked-bar-chart', 'figure'),
    Output('stacked-bar-chart-header', 'children')],
    [Input('continent-dropdown', 'value'),
     Input('subregion-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('year-slider', 'value'),
     Input('month-dropdown', 'value'),
     Input('disaster-type-checkbox', 'value')]
)
def plot_bar_total_disaster(selected_continent, selected_subregion, selected_country, selected_year, selected_month, selected_disaster_type):
    # Update the plot card header name
    base_header = "Trends of "
    card_header_text = generate_header(base_header, selected_disaster_type, selected_year, selected_month)
    
    # Use the helper function to filter data
    filtered_data = apply_filters(data, selected_continent, selected_subregion, selected_country, selected_year, selected_month, selected_disaster_type)

    # Group by year and type for the filtered data
    disasters_type_and_year = filtered_data.groupby(['year', 'type']).size().reset_index(name='total_disasters')

    # Convert 'year' to int
    disasters_type_and_year['year'] = disasters_type_and_year['year'].astype(int)
    
    # Map the colors based on the disaster type
    disaster_colors = {
        'Drought': '#4C230A', 'Extreme temperature': '#E34B48', 'Volcanic activity': '#0D160B', 'Wildfire': 'orange', 
        'Earthquake': '#555B6E', 'Mass movement': '#84B59F', 'Flood': '#568EA3', 'Storm' : '#BBE5ED'}
    
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
            y=-0.2,
            xanchor="right",
            x=1
        )
    )
    return fig, card_header_text

# Chart-B: Total death by year
@app.callback(
    [Output('casualty-trend', 'figure'),
    Output('casualty-trend-header', 'children')],
    [Input('continent-dropdown', 'value'),
     Input('subregion-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('year-slider', 'value'),
     Input('month-dropdown', 'value'),
     Input('disaster-type-checkbox', 'value')]
)


def plot_line_casualty_trend(selected_continent, selected_subregion, selected_country, selected_year, selected_month, selected_disaster_type):
    # Update the plot card header name
    base_header = "Number of deaths from "
    card_header_text = generate_header(base_header, selected_disaster_type, selected_year, selected_month)
    
    # Use the helper function to filter data
    filtered_data = apply_filters(data, selected_continent, selected_subregion, selected_country, selected_year, selected_month, selected_disaster_type)

    # Group by year and country to calculate total deaths
    deaths_by_country_year = filtered_data.groupby(['year', 'country'])['total_deaths'].sum().reset_index()
    
    # Convert 'year' to int
    deaths_by_country_year['year'] = deaths_by_country_year['year'].astype(int)

    # Create the line chart for Casualty Trend
    fig = px.line(
        deaths_by_country_year,
        x='year',
        y='total_deaths',
        color='country',  # Differentiate countries
        labels={'total_deaths': 'Total Deaths', 'year': 'Year'},
        line_group='country'  # Ensure separate lines for each country
    )

    # Customize the hover information to show only the relevant country
    for trace in fig.data:
        trace.hovertemplate = f'{trace.name}<br>Year: %{{x}}<br>Total Deaths: %{{y}}<extra></extra>'

    # Customize the layout of the line chart
    fig.update_layout(
        xaxis=dict(
            title='Year',
            tickvals=[i for i in range(2000, 2025, 4)]
        ),
        yaxis = dict(
            title='Total Deaths',  
            showgrid=True, gridwidth=1, gridcolor='black', griddash = 'dash'
        ),
        plot_bgcolor='white',
        margin=dict(l=40, r=40, t=40, b=40),
        showlegend=False  # Hide the legend
    )

    return fig, card_header_text

# Run the app
# Unhash below to make it automatically open the dashboard in browser when running py app.
# def open_browser():
    # webbrowser.open_new("http://127.0.0.1:8050/")

# Only open the browser if the script is run directly
if __name__ == "__main__":
    # Start the Dash app and open the browser automatically after a slight delay
    # Timer(1, open_browser).start()
    app.run_server(debug=True)