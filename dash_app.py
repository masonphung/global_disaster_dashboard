import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the dataset
file_path = 'C:/Users/admin/Downloads/try_dash/cleaned_emrat.xlsx'
data = pd.read_excel(file_path)

# Convert the 'last_update' column to datetime
data['last_update'] = pd.to_datetime(data['last_update'], errors='coerce')

# Prepare data: Calculate key statistics
total_deaths = data['total_deaths'].sum()
total_affected = data['total_affected'].sum()
total_damage = data['total_damage'].sum()

most_deaths_country = data.groupby('country')['total_deaths'].sum().idxmax()
most_affected_country = data.groupby('country')['total_affected'].sum().idxmax()
most_damaged_country = data.groupby('country')['total_damage'].sum().idxmax()

# Calculate last updated date
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

# Create the Dash app
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    html.H1('Global Disaster Statistics'),

    # Filters in the same row
    html.Div([
        # Filter 1: Year and Month (Year above Month)
        html.Div([
            html.Label('Year'),
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': str(y), 'value': str(y)} for y in years],
                placeholder='Select Year'
            ),
            html.Label('Month'),
            dcc.Dropdown(
                id='month-dropdown',
                options=[{'label': str(m), 'value': str(m)} for m in months],
                placeholder='Select Month'
            )
        ], style={'width': '30%', 'display': 'inline-block'}),

        # Filter 2: Location (Continent, Subregion, Country in vertical stack)
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
        ], style={'width': '30%', 'display': 'inline-block', 'padding-left': '10px'}),

        # Filter 3: Disaster Type
        html.Div([
            html.Label('Disaster Type'),
            dcc.Dropdown(
                id='disaster-type-dropdown',
                options=[{'label': dt, 'value': dt} for dt in disaster_types],
                placeholder='Select Disaster Type'
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding-left': '10px'})
    ], style={'display': 'flex', 'flex-direction': 'row', 'padding': '20px'}),

    # Row for Total Deaths, Total Affected, Total Damage (above the maps)
    html.Div([
        html.Div([
            html.H3('Total Deaths'),
            html.P(id='total-deaths-card', children=f"{total_deaths:,}")
        ], style={'width': '33%', 'display': 'inline-block', 'border': '1px solid #ccc', 'padding': '20px', 'box-sizing': 'border-box'}),

        html.Div([
            html.H3('Total Affected'),
            html.P(id='total-affected-card', children=f"{total_affected:,}")
        ], style={'width': '33%', 'display': 'inline-block', 'border': '1px solid #ccc', 'padding': '20px', 'box-sizing': 'border-box'}),

        html.Div([
            html.H3('Total Damage'),
            html.P(id='total-damage-card', children=f"{total_damage:,}")
        ], style={'width': '33%', 'display': 'inline-block', 'border': '1px solid #ccc', 'padding': '20px', 'box-sizing': 'border-box'})
    ], style={'display': 'flex', 'flex-direction': 'row', 'padding-top': '20px'}),

    # Row for two maps
    html.Div([
        dcc.Graph(id='damage-map', style={'width': '50%', 'height': '500px'}),
        dcc.Graph(id='disaster-count-map', style={'width': '50%', 'height': '500px'})
    ], style={'display': 'flex', 'flex-direction': 'row'}),

    # Row for the four remaining cards (below maps but above bar and line chart)
    html.Div([
        html.Div([
            html.H3('Most Affected Country'),
            html.P(id='most-affected-country-card', children=most_affected_country)
        ], style={'width': '25%', 'display': 'inline-block', 'border': '1px solid #ccc', 'padding': '20px', 'box-sizing': 'border-box'}),

        html.Div([
            html.H3('Most Damaged Country'),
            html.P(id='most-damaged-country-card', children=most_damaged_country)
        ], style={'width': '25%', 'display': 'inline-block', 'border': '1px solid #ccc', 'padding': '20px', 'box-sizing': 'border-box'}),

        html.Div([
            html.H3('Country with Most Deaths'),
            html.P(id='most-deaths-country-card', children=most_deaths_country)
        ], style={'width': '25%', 'display': 'inline-block', 'border': '1px solid #ccc', 'padding': '20px', 'box-sizing': 'border-box'}),

        html.Div([
            html.H3('Last Updated'),
            html.P(id='last-updated-card', children=last_updated.strftime('%Y-%m-%d'))
        ], style={'width': '25%', 'display': 'inline-block', 'border': '1px solid #ccc', 'padding': '20px', 'box-sizing': 'border-box'})
    ], style={'display': 'flex', 'flex-direction': 'row', 'padding-top': '20px'}),

    # Row for Stacked Bar Chart and Line Graph (Casualty Trend)
    html.Div([
        dcc.Graph(id='stacked-bar-chart', style={'width': '50%', 'height': '500px'}),
        dcc.Graph(id='casualty-trend', style={'width': '50%', 'height': '500px'})  # Added Casualty Trend line graph
    ], style={'display': 'flex', 'flex-direction': 'row', 'padding-top': '20px'}),
])

# Callbacks remain in original order

# Callback to update the subregion dropdown based on selected continent
@app.callback(
    Output('subregion-dropdown', 'options'),
    Input('continent-dropdown', 'value')
)
def update_subregions(selected_continent):
    if selected_continent:
        filtered_subregions = data[data['region'] == selected_continent]['subregion'].unique()
        return [{'label': s, 'value': s} for s in filtered_subregions]
    return []

# Callback to update the country dropdown based on selected subregion
@app.callback(
    Output('country-dropdown', 'options'),
    Input('subregion-dropdown', 'value')
)
def update_countries(selected_subregion):
    if selected_subregion:
        filtered_countries = data[data['subregion'] == selected_subregion]['country'].unique()
        return [{'label': c, 'value': c} for c in filtered_countries]
    return []

# Callback for updating the total deaths, total affected, and total damage cards
@app.callback(
    [Output('total-deaths-card', 'children'),
     Output('total-affected-card', 'children'),
     Output('total-damage-card', 'children')],
    [Input('continent-dropdown', 'value'),
     Input('subregion-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value'),
     Input('disaster-type-dropdown', 'value')]
)
def update_stat_cards(selected_continent, selected_subregion, selected_country, selected_year, selected_month, selected_disaster_type):
    filtered_data = data
    
    # Apply continent filter
    if selected_continent:
        filtered_data = filtered_data[filtered_data['region'] == selected_continent]

    # Apply subregion filter
    if selected_subregion:
        filtered_data = filtered_data[filtered_data['subregion'] == selected_subregion]

    # Apply country filter
    if selected_country:
        filtered_data = filtered_data[filtered_data['country'] == selected_country]

    # Apply year filter
    if selected_year:
        filtered_data = filtered_data[filtered_data['year'] == int(selected_year)]
    
    # Apply month filter
    if selected_month:
        filtered_data = filtered_data[filtered_data['month'] == int(selected_month)]

    # Apply disaster type filter
    if selected_disaster_type:
        filtered_data = filtered_data[filtered_data['type'] == selected_disaster_type]

    # Calculate totals for the filtered data
    total_deaths = filtered_data['total_deaths'].sum()
    total_affected = filtered_data['total_affected'].sum()
    total_damage = filtered_data['total_damage'].sum()

    # Format the values with commas for better readability
    return (f"{total_deaths:,}", f"{total_affected:,}", f"{total_damage:,}")

# Callback for updating the four remaining cards: Most Affected, Most Damaged, Country with Most Deaths, Last Updated
@app.callback(
    [Output('most-affected-country-card', 'children'),
     Output('most-damaged-country-card', 'children'),
     Output('most-deaths-country-card', 'children'),
     Output('last-updated-card', 'children')],
    [Input('continent-dropdown', 'value'),
     Input('subregion-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value'),
     Input('disaster-type-dropdown', 'value')]
)
def update_remaining_cards(selected_continent, selected_subregion, selected_country, selected_year, selected_month, selected_disaster_type):
    filtered_data = data
    
    # Apply continent filter
    if selected_continent:
        filtered_data = filtered_data[filtered_data['region'] == selected_continent]

    # Apply subregion filter
    if selected_subregion:
        filtered_data = filtered_data[filtered_data['subregion'] == selected_subregion]

    # Apply country filter
    if selected_country:
        filtered_data = filtered_data[filtered_data['country'] == selected_country]

    # Apply year filter
    if selected_year:
        filtered_data = filtered_data[filtered_data['year'] == int(selected_year)]

    # Apply month filter
    if selected_month:
        filtered_data = filtered_data[filtered_data['month'] == int(selected_month)]

    # Apply disaster type filter
    if selected_disaster_type:
        filtered_data = filtered_data[filtered_data['type'] == selected_disaster_type]

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

# Callback to create and update the total damage choropleth map based on filters
@app.callback(
    Output('damage-map', 'figure'),
    [Input('continent-dropdown', 'value'),
     Input('subregion-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value'),
     Input('disaster-type-dropdown', 'value')]
)
def update_damage_map(selected_continent, selected_subregion, selected_country, selected_year, selected_month, selected_disaster_type):
    filtered_data = data
    
    # Apply continent filter
    if selected_continent:
        filtered_data = filtered_data[filtered_data['region'] == selected_continent]
    
    # Apply subregion filter
    if selected_subregion:
        filtered_data = filtered_data[filtered_data['subregion'] == selected_subregion]
    
    # Apply country filter
    if selected_country:
        filtered_data = filtered_data[filtered_data['country'] == selected_country]
    
    # Apply year filter
    if selected_year:
        filtered_data = filtered_data[filtered_data['year'] == int(selected_year)]
    
    # Apply month filter
    if selected_month:
        filtered_data = filtered_data[filtered_data['month'] == int(selected_month)]

    # Apply disaster type filter
    if selected_disaster_type:
        filtered_data = filtered_data[filtered_data['type'] == selected_disaster_type]

    # Create choropleth map for total damage
    fig = px.choropleth(
        data_frame=filtered_data,
        locations='country',
        locationmode='country names',
        color='total_damage',
        hover_name='country',
        color_continuous_scale='Viridis',
        labels={'total_damage': 'Total Damage (in USD)'},
        title="Total Damage by Country"
    )

    fig.update_geos(
        showcoastlines=True,
        coastlinecolor="Black",
        showland=True, landcolor="lightgray",
        showocean=True, oceancolor="lightblue",
        projection_type="natural earth"
    )

    return fig

# Callback to create and update the disaster count choropleth map based on filters
@app.callback(
    Output('disaster-count-map', 'figure'),
    [Input('continent-dropdown', 'value'),
     Input('subregion-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value'),
     Input('disaster-type-dropdown', 'value')]
)
def update_disaster_count_map(selected_continent, selected_subregion, selected_country, selected_year, selected_month, selected_disaster_type):
    filtered_data = data
    
    # Apply continent filter
    if selected_continent:
        filtered_data = filtered_data[filtered_data['region'] == selected_continent]
    
    # Apply subregion filter
    if selected_subregion:
        filtered_data = filtered_data[filtered_data['subregion'] == selected_subregion]
    
    # Apply country filter
    if selected_country:
        filtered_data = filtered_data[filtered_data['country'] == selected_country]

    # Apply year filter
    if selected_year:
        filtered_data = filtered_data[filtered_data['year'] == int(selected_year)]
    
    # Apply month filter
    if selected_month:
        filtered_data = filtered_data[filtered_data['month'] == int(selected_month)]

    # Apply disaster type filter
    if selected_disaster_type:
        filtered_data = filtered_data[filtered_data['type'] == selected_disaster_type]

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
        labels={'total_disasters': 'Total Number of Disasters'},
        title="Total Number of Disasters by Country"
    )

    fig.update_geos(
        showcoastlines=True,
        coastlinecolor="Black",
        showland=True, landcolor="lightgray",
        showocean=True, oceancolor="lightblue",
        projection_type="natural earth"
    )

    return fig

# Callback to create and update the stacked bar chart based on filters
@app.callback(
    Output('stacked-bar-chart', 'figure'),
    [Input('continent-dropdown', 'value'),
     Input('subregion-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value'),
     Input('disaster-type-dropdown', 'value')]
)
def update_stacked_bar_chart(selected_continent, selected_subregion, selected_country, selected_year, selected_month, selected_disaster_type):
    filtered_data = data
    
    # Apply continent filter
    if selected_continent:
        filtered_data = filtered_data[filtered_data['region'] == selected_continent]
    
    # Apply subregion filter
    if selected_subregion:
        filtered_data = filtered_data[filtered_data['subregion'] == selected_subregion]
    
    # Apply country filter
    if selected_country:
        filtered_data = filtered_data[filtered_data['country'] == selected_country]
    
    # Apply year filter
    if selected_year:
        filtered_data = filtered_data[filtered_data['year'] == int(selected_year)]
    
    # Apply month filter
    if selected_month:
        filtered_data = filtered_data[filtered_data['month'] == int(selected_month)]

    # Apply disaster type filter
    if selected_disaster_type:
        filtered_data = filtered_data[filtered_data['type'] == selected_disaster_type]

    # Group by year and type for the filtered data
    disasters_by_type_and_year_filtered = filtered_data.groupby(['year', 'type']).size().reset_index(name='total_disasters')

    # Create stacked bar chart for total disasters by type and year
    fig = px.bar(
        disasters_by_type_and_year_filtered,
        x='year',
        y='total_disasters',
        color='type',
        labels={'total_disasters': 'Total Disasters'},
        title="Total Number of Disasters by Year and Type"
    )
    
    return fig

# Callback for Casualty Trend (Line Graph)
@app.callback(
    Output('casualty-trend', 'figure'),
    [Input('continent-dropdown', 'value'),
     Input('subregion-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value'),
     Input('disaster-type-dropdown', 'value')]
)
def update_casualty_trend(selected_continent, selected_subregion, selected_country, selected_year, selected_month, selected_disaster_type):
    filtered_data = data

    # Apply continent filter
    if selected_continent:
        filtered_data = filtered_data[filtered_data['region'] == selected_continent]

    # Apply subregion filter
    if selected_subregion:
        filtered_data = filtered_data[filtered_data['subregion'] == selected_subregion]

    # Apply country filter
    if selected_country:
        filtered_data = filtered_data[filtered_data['country'] == selected_country]

    # Apply year filter
    if selected_year:
        filtered_data = filtered_data[filtered_data['year'] == int(selected_year)]

    # Apply month filter
    if selected_month:
        filtered_data = filtered_data[filtered_data['month'] == int(selected_month)]

    # Apply disaster type filter
    if selected_disaster_type:
        filtered_data = filtered_data[filtered_data['type'] == selected_disaster_type]

    # Group by year and calculate total deaths
    deaths_by_year = filtered_data.groupby('year')['total_deaths'].sum().reset_index()

    # Create the line chart for Casualty Trend
    fig = px.line(
        deaths_by_year,
        x='year',
        y='total_deaths',
        title="Casualty Trend: Total Deaths by Year",
        labels={'total_deaths': 'Total Deaths', 'year': 'Year'},
    )

    # Customize the layout of the line chart
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Total Deaths',
        plot_bgcolor='white',
        hovermode='x unified',
        margin=dict(l=40, r=40, t=40, b=40)
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
