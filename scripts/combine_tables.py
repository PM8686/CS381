import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('../nyc.db')  # Replace with your database path

# Load the tables into pandas DataFrames
weather_df = pd.read_sql_query("SELECT * FROM nyc_weather_hourly_cleaned", conn)
energy_df = pd.read_sql_query("SELECT * FROM nyc_energy_hourly_cleaned", conn)

# make sure column names are the same (year, month, day, hour)
energy_df.rename(columns={"Year": "year", "Month": "month", "Day": "day"}, inplace=True)

# Convert 'hour' columns to int for consistency
weather_df['hour'] = weather_df['hour'].astype(int)
# Drop rows where 'hour' is NaN
# Get the number of rows before dropping NaN values
rows_before = energy_df.shape[0]
# Drop rows where 'hour' is NaN
energy_df = energy_df.dropna(subset=['hour'])
# Get the number of rows after dropping NaN values
rows_after = energy_df.shape[0]
# Calculate the number of rows dropped
rows_dropped = rows_before - rows_after
# Print the number of rows dropped
# print(f"Number of rows dropped: {rows_dropped} out of {rows_after} a {(rows_dropped*1.0)/rows_before * 100} percent decrease") # Number of rows dropped: 768 out of 176614 a %0.4329638858508755 percent decrease
energy_df['hour'] = energy_df['hour'].astype(int)

# Merge the two DataFrames on the common columns: year, month, day, and hour
merged_df = pd.merge(weather_df, energy_df, how='inner', 
                       on=['year', 'month', 'day', 'hour'])

# Drop the '_y' columns
merged_df = merged_df.loc[:, ~merged_df.columns.str.endswith('_y')]
# Rename '_x' columns
merged_df = merged_df.rename(columns=lambda x: x.rstrip('_x') if x.endswith('_x') else x)
# Make hours ints
energy_df['hour'] = energy_df['hour'].astype(int)

# Show the first 10 rows of the combined DataFrame
# print(merged_df.head(10))

# Save the merged DataFrame to a new table in the SQLite database
merged_df.to_sql('nyc_hourly_merged', conn, if_exists='replace', index=False)

# Close the connection to the database
conn.close()
