import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar
import sqlite3
import matplotlib.pyplot as plt
import numpy as np

# Connect to your database
conn = sqlite3.connect('../../nyc.db')

# Read nyc_energy table
nyc_energy = pd.read_sql_query("SELECT * FROM nyc_energy", conn)

# Convert Time_Stamp to datetime
nyc_energy["Time_Stamp"] = pd.to_datetime(nyc_energy["Time_Stamp"], format="%m/%d/%Y %H:%M:%S")

# Keep all columns (no dropping), but create additional time-based features
nyc_energy["hour"] = nyc_energy["Time_Stamp"].dt.hour
nyc_energy["day_of_week"] = nyc_energy["Time_Stamp"].dt.dayofweek  # Monday = 0, Sunday = 6
nyc_energy["is_weekend"] = (nyc_energy["day_of_week"] >= 5).astype(int)
nyc_energy["Year"] = nyc_energy["Time_Stamp"].dt.year.astype(int)
nyc_energy["Month"] = nyc_energy["Time_Stamp"].dt.month.astype(int)
nyc_energy["Day"] = nyc_energy["Time_Stamp"].dt.day.astype(int)
nyc_energy["hour"] = nyc_energy["hour"].astype(int)

# Holiday Feature
cal = USFederalHolidayCalendar()
holidays = cal.holidays(start=nyc_energy["Time_Stamp"].min(), end=nyc_energy["Time_Stamp"].max())
nyc_energy["is_holiday"] = nyc_energy["Time_Stamp"].dt.normalize().isin(holidays).astype(int)

# Remove Name Column (as always N.Y.C)
nyc_energy = nyc_energy.drop(columns=["Name"])

# Try coercing Load to numeric 
load_numeric = pd.to_numeric(nyc_energy["Load"], errors="coerce")
bad_rows = nyc_energy[load_numeric.isna()]
print("Bad rows (non-numeric Load values):")
print(bad_rows)

# Replace Load with numeric and drop NaNs
nyc_energy["Load"] = load_numeric
nyc_energy = nyc_energy.dropna(subset=["Load"])
# IQR-based Outlier Removal
before = len(nyc_energy)

# Q1 = nyc_energy["Load"].quantile(0.25)
# Q3 = nyc_energy["Load"].quantile(0.75)
# IQR = Q3 - Q1
# lower_bound = Q1 - 2 * IQR
# upper_bound = Q3 + 2 * IQR

 # only replacing 0s and NaNs
lower_bound = 100
# upper_bound = np.inf
print("To remove outlier 0s - lower_bound: " + str(lower_bound))
# print("upper_bound: " + str(upper_bound))

nyc_energy = nyc_energy[
    (nyc_energy["Load"] >= lower_bound)
]

after = len(nyc_energy)

print(f"Rows before cleaning: {before}")
print(f"Rows after cleaning: {after}")
print(f"Total rows dropped: {before - after}")

# Save the fully-featured cleaned table into the database
nyc_energy.to_sql("nyc_energy_cleaned", conn, if_exists="replace", index=False)


# # Plot Load distribution before and after cleaning
# fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# # Plot before cleaning
# axes[0].hist(load_numeric.dropna(), bins=100, color='skyblue', edgecolor='black')
# axes[0].set_title('Load Distribution Before Cleaning')
# axes[0].set_xlabel('Load')
# axes[0].set_ylabel('Frequency')

# # Plot after cleaning
# axes[1].hist(nyc_energy["Load"], bins=100, color='salmon', edgecolor='black')
# axes[1].set_title('Load Distribution After Cleaning')
# axes[1].set_xlabel('Load')
# axes[1].set_ylabel('Frequency')

# plt.tight_layout()
# plt.show()

# Now Set Time_Stamp as index 
nyc_energy_hourly = nyc_energy.set_index("Time_Stamp")

# Drop Time column
nyc_energy_hourly = nyc_energy_hourly.drop(columns=["Time"])

# Define how each column should be aggregated
agg_dict = {
    "Load": "mean",
    "Year": "first",
    "Month": "first",
    "Day": "first",
    "hour": "first",
    "day_of_week": "first",
    "is_weekend": "first",
    "is_holiday": "first"
}

# Resample and aggregate
nyc_energy_hourly = nyc_energy_hourly.resample('h').agg(agg_dict)

# Reset index
nyc_energy_hourly = nyc_energy_hourly.reset_index()

# # Reset hour, day_of_week, is_weekend, is_holiday to integers
# nyc_energy_hourly["hour"] = nyc_energy_hourly["hour"].astype(int)
# nyc_energy_hourly["day_of_week"] = nyc_energy_hourly["day_of_week"].astype(int)
# nyc_energy_hourly["is_weekend"] = nyc_energy_hourly["is_weekend"].astype(int)
# nyc_energy_hourly["is_holiday"] = nyc_energy_hourly["is_holiday"].astype(int)

# Drop Time Stamp column
nyc_energy_hourly = nyc_energy_hourly.drop(columns=["Time_Stamp"])

# Save the hourly-aggregated table to a new table in the database
nyc_energy_hourly.to_sql("nyc_energy_hourly_cleaned", conn, if_exists="replace", index=False)

# Done
conn.close()
