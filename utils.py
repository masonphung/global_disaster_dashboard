# The file includes function(s) that help to run the dash app.
# They help manipulate data and reduce repeating codes.
import dash_bootstrap_components as dbc
from dash import dcc, html

## A function that helps to filter data when plotting
def apply_filters(data, selected_continent=None, selected_subregion=None, 
                  selected_country=None, selected_year=None, selected_month=None, 
                  selected_disaster_type=None):
    """
    Apply a series of filters to the disaster data based on user-selected criteria.

    Parameters:
    - data (DataFrame): The input DataFrame containing disaster statistics.
    - selected_continent (str, optional): The continent to filter by. Defaults to None.
    - selected_subregion (str, optional): The subregion to filter by. Defaults to None.
    - selected_country (str, optional): The country to filter by. Defaults to None.
    - selected_year (list, optional): A list containing two integers representing the range of years to filter by. 
                                       Defaults to None.
    - selected_month (int, optional): The month to filter by. Defaults to None.
    - selected_disaster_type (str, optional): The type of disaster to filter by. Defaults to None.

    Returns:
    - DataFrame: A filtered DataFrame containing only the rows that meet the specified criteria.
    """
    filtered_data = data.copy()
    
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
        filtered_data = filtered_data[
            (filtered_data['year'] >= str(selected_year[0])) &
            (filtered_data['year'] <= str(selected_year[1]))
        ]
    
    # Apply month filter
    if selected_month:
        filtered_data = filtered_data[filtered_data['month'] == int(selected_month)]
    
    # Apply disaster type filter
    if selected_disaster_type:  # Ensure this is not None or empty
        filtered_data = filtered_data[filtered_data['type'].isin(selected_disaster_type)]

    return filtered_data


def generate_header(header_text, selected_disasters, selected_year, selected_month):
    """
    Generate a dynamic header string based on selected disasters, years, and months.

    Parameters:
    - base_header_text (str): The base text for the header.
    - selected_disasters (list): A list of selected disaster types.
    - selected_year (int or list): The selected year or a range of years as a list.
    - selected_month (int): The selected month as a number (1-12).

    Returns:
        str: A formatted header string reflecting the selections appended to the base text.
    """

    # Disaster names logic
    if len(selected_disasters) == 1:
        header_text += f"{selected_disasters[0]}"
    elif len(selected_disasters) == 2:
        header_text += f"{selected_disasters[0]} and {selected_disasters[1]}"
    else:
        header_text += "disasters"

    # Year or range of years logic
    if isinstance(selected_year, list):  # If it's a year range
        if selected_year[0] != selected_year[1]:
            header_text += f", {selected_year[0]} to {selected_year[1]}"
        else:
            header_text += f" in {selected_year[0]}"
    elif selected_year is not None:
        header_text += f" in {selected_year}"
    
    # Month logic
    month_map = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }
    if selected_month:
        header_text += f" in {month_map[selected_month]}"

    return header_text

# Change the int value into a shorter format
def format_value(value):
    if value is None:
        return "N/A"
    elif value < 1_000:
        return f"{value:.0f}"  # No suffix for values below 1K
    elif value < 1_000_000:
        return f"{value / 1_000:.1f}K"  # Thousands
    elif value < 1_000_000_000:
        return f"{value / 1_000_000:.1f}M"  # Millions
    else:
        return f"{value / 1_000_000_000:.1f}B"  # Billions
    
color_list = [
    '#4C230A', '#555B6E', '#C44802', '#568EA3', '#84B59F', '#BBE5ED','#0D160B', 'orange',
    '#9DCBBA', '#5E8C61', '#132A13', '#00BD9D', '#285943','#247BA0', '#38726C', '#1446A0', '#5C2751',
    '#586A6A', '#092327', '#64113F', '#26532B', '#531CB3', '#002A32', '#749C75', '#473144', '#514B23',
    '#5C415D', '#1B998B', '#7C7287', '#DC136C', '#637081', '#628B48', '#B388EB', '#EC4E20', '#114B5F'
]

map_color = ['#96BBBB', '#FEDC85', '#FEB945', '#C44802', '#712805']