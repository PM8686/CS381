import sqlite3
import pandas as pd
import numpy as np

# Connect to the SQLite database
conn = sqlite3.connect('../nyc.db')  # Replace with your database path

# Load the tables into pandas DataFrames
merged_df = pd.read_sql_query("SELECT * FROM nyc_hourly_merged", conn)

print(f"Shape before feature engineering: {merged_df.shape}")

# Add Lag Features
# Create a datetime column and sort
merged_df['datetime'] = pd.to_datetime(merged_df[['year', 'month', 'day', 'hour']])
merged_df = merged_df.sort_values('datetime').reset_index(drop=True)

# Check for time continuity using .diff()
time_diff = merged_df['datetime'].diff()
time_diff24 = merged_df['datetime'].diff(24)

# Mask for rows with proper 1-hour and 24-hour continuity
good_rows = (time_diff == pd.Timedelta(hours=1)) & (time_diff24 == pd.Timedelta(hours=24))

# Shift and create lag features (done on full data)
merged_df['Load_lag1'] = merged_df['Load'].shift(1)
merged_df['Load_lag24'] = merged_df['Load'].shift(24)

# Keep only rows with valid time continuity AND non-null lags
lagged_df = merged_df[good_rows].dropna(subset=['Load_lag1', 'Load_lag24']).reset_index(drop=True)

# remove datetime
lagged_df = lagged_df.drop(columns=["datetime"])

# Show how many were removed
rows_removed = merged_df.shape[0] - lagged_df.shape[0]
print(f"Rows removed for lag + continuity: {rows_removed} ({rows_removed / merged_df.shape[0] * 100:.2f}%)")
print(f"Shape after lag feature filtering: {lagged_df.shape}")

# Add season feature
def get_season(month):
    if month in [12, 1, 2]: return 0  # winter
    elif month in [3, 4, 5]: return 1  # spring
    elif month in [6, 7, 8]: return 2  # summer
    else: return 3  # fall

lagged_df['season'] = lagged_df['month'].apply(get_season)

# show new features
print(lagged_df.head())
print(f"Shape after feature engineering: {lagged_df.shape}")

# Save the merged DataFrame to a new table in the SQLite database
lagged_df.to_sql('nyc_hourly_merged_added', conn, if_exists='replace', index=False)

# Close the connection to the database
conn.close()
