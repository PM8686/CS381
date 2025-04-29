import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar
import sqlite3

# Connect to your database
conn = sqlite3.connect('../../nyc.db')

# Read nyc_weather_hourly table
nyc_weather = pd.read_sql_query("SELECT * FROM nyc_weather_hourly", conn)

# Convert 'date' to datetime and handle timezone
nyc_weather["date"] = pd.to_datetime(nyc_weather["date"], utc=True, errors='coerce')

# Drop the timezone information (if you want to standardize to UTC)
nyc_weather["date"] = nyc_weather["date"].dt.tz_localize(None)

# Create additional time-based features
nyc_weather_cleaned = nyc_weather.copy()
nyc_weather_cleaned["hour"] = nyc_weather_cleaned["date"].dt.hour
# nyc_weather_cleaned["time"] = nyc_weather_cleaned["date"].dt.time [already by hour]
nyc_weather_cleaned["day_of_week"] = nyc_weather_cleaned["date"].dt.dayofweek  # Monday = 0, Sunday = 6
nyc_weather_cleaned["is_weekend"] = nyc_weather_cleaned["day_of_week"] >= 5
nyc_weather_cleaned["year"] = nyc_weather_cleaned["date"].dt.year
nyc_weather_cleaned["month"] = nyc_weather_cleaned["date"].dt.month
nyc_weather_cleaned["day"] = nyc_weather_cleaned["date"].dt.day

# Holiday Feature
cal = USFederalHolidayCalendar()
holidays = cal.holidays(start=nyc_weather_cleaned["date"].min(), end=nyc_weather_cleaned["date"].max())
nyc_weather_cleaned["is_holiday"] = nyc_weather_cleaned["date"].dt.normalize().isin(holidays)

# Drop unneccessary columns
nyc_weather_cleaned = nyc_weather_cleaned.drop(columns=["date"])

# Save the cleaned table to a new table in the database
nyc_weather_cleaned.to_sql("nyc_weather_hourly_cleaned", conn, if_exists="replace", index=False)

# Close the database connection
conn.close()
