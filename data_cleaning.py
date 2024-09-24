# import libraries
import pandas as pd
import numpy as np
import datetime

# Load raw data
df = pd.read_excel('dataset/raw_data/public_emdat_20240923.xlsx')

# Choose desired variables
data = df[["DisNo.", "Disaster Type", "ISO", "Country", "Subregion", "Region", "Start Year", "Start Month", 
             "Total Deaths", "Total Affected", "Total Damage, Adjusted ('000 US$)", "Last Update"]]

# Rename the columns
data.rename(
    columns = {
        "DisNo.": "id", "Disaster Type": "type", "ISO": "iso", "Country": "country", 
        "Subregion": "subregion", "Region": "region", "Start Year": "year", "Start Month": "month", 
        "Total Deaths": "total_deaths", "Total Affected": "total_affected", 
        "Total Damage, Adjusted ('000 US$)": "total_damage", "Last Update": "last_update"
    },
    inplace = True
)


# Drop non-natural disaster and disasters that only have 1 (not enough) observations
remove_vars = ['Animal incident', 'Epidemic', 'Impact', 'Infestation']
data = data[~data['type'].isin(remove_vars)]

# Remove observations with null Month
data = data[~data['month'].isnull()]

# Convert null values in total damage, deaths and affected to '-1'
for i in ['total_damage', 'total_deaths', 'total_affected']:
    data[i] = data[i].replace(np.nan, -1)


# Add a yyyy/mm variable
data['date'] = data.apply(lambda row: f"{int(row['year'])}/{int(row['month']):02d}", axis=1)

# Define the mapping for disaster types
disaster_mapping = {
    'Flood': 'Flood',
    'Glacial lake outburst flood': 'Flood',
    'Mass movement (wet)': 'Mass movement',
    'Mass movement (dry)': 'Mass movement',
    'Drought': 'Drought',
    'Extreme temperature': 'Extreme temperature',
    'Volcanic activity': 'Volcanic activity',
    'Storm': 'Storm',
    'Wildfire': 'Wildfire',
    'Earthquake': 'Earthquake'
}

# Group the disaster types with defined mapping
data['type'] = data['type'].map(disaster_mapping)

# Now map each disaster type to an integer code
type_codes = {
    'Drought': 1,
    'Flood': 2,
    'Extreme temperature': 3,
    'Volcanic activity': 4,
    'Storm': 5,
    'Wildfire': 6,
    'Earthquake': 7,
    'Mass movement': 8
}

# Create a new column 'type_code' by mapping the disaster types to their integer codes
data['type_code'] = data['type'].map(type_codes)

# Export the final data
out_path = "dataset/cleaned_emrat.xlsx"
writer = pd.ExcelWriter(out_path , engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1')
