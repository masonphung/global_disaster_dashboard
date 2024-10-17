# import libraries
import pandas as pd
import numpy as np
import datetime

def load_data(file_path, max_attempts=3):
    attempts = 0
    while attempts < max_attempts:
        try:
            # Try to load the data
            df = pd.read_excel(file_path, index_col = False)
            return df  # If successful, return the DataFrame
        except FileNotFoundError:
            # If file is not found, increment the attempt counter
            attempts += 1
            print(f"File not found: {file_path} (Attempt {attempts} of {max_attempts})")
            
            # If max attempts reached, exit the loop
            if attempts == max_attempts:
                print("Maximum attempts reached. Exiting...")
                return None
            
            # Prompt user for a new path
            file_path = input("Please enter the correct file path: ")

# The original file path
file_path = 'dataset/backups/raw_data/public_emdat_20240923.xlsx'
df = load_data(file_path)

if df is not None:
    print("File loaded successfully.")
else:
    print("Failed to load the file after 3 attempts, make sure you are choosing the relative file path.")

# Choose desired variables and make a copy to avoid the warning
data = df[["DisNo.", "Disaster Type", "ISO", "Country", "Subregion", "Region", 
            #"Latitude", "Longitude", 
            "Start Year", "Start Month", 
            "Total Deaths", "Total Affected", "Total Damage, Adjusted ('000 US$)", "Last Update"]].copy()

# Rename the columns
data.rename(
    columns = {
        "DisNo.": "id", "Disaster Type": "type", "ISO": "iso", "Country": "country", 
        "Subregion": "subregion", "Region": "region", 
        #"Latitude": "latitude", "Longitude": "logitude",
        "Start Year": "year", "Start Month": "month", 
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
# for i in ['total_damage', 'total_deaths', 'total_affected']:
#    data[i] = data[i].replace(np.nan, -1)

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
# Disaster types but in number
data['type_code'] = data['type'].map(type_codes)

# Export the final data (with disaster events retained and categorized by country-wide total damage)
data.to_excel("dataset/cleaned_emrat.xlsx", index = False)

print("Data cleaned and saved successfully!")


