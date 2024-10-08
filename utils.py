# The file includes function(s) that help to run the dash app.
# They help manipulate data and reduce repeating codes.


## A function that helps to filter data when plotting
def apply_filters(data, selected_continent=None, selected_subregion=None, 
                  selected_country=None, selected_year=None, selected_month=None, selected_disaster_type=None):
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
            (filtered_data['year'] >= str(selected_year[0]))
            &
            (filtered_data['year'] <= str(selected_year[1]))
        ]
    # Apply month filter
    if selected_month:
        filtered_data = filtered_data[filtered_data['month'] == int(selected_month)]
    # Apply disaster type filter
    if selected_disaster_type:  # Ensure this is not None or empty
        filtered_data = filtered_data[filtered_data['type'].isin(selected_disaster_type)]
    return filtered_data