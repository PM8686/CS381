import os
import sqlite3
import csv

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # This script's directory
CSV_PATH = os.path.join(BASE_DIR, 'nyc_weather_hourly.csv')
DB_PATH = os.path.join(BASE_DIR, '../nyc.db')

# Create a connection to the SQLite database
conn = sqlite3.connect(DB_PATH)
db = conn.cursor()

# Import CSV into the table
with open(CSV_PATH, 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # Skip the header row

    for row in reader:
        db.execute('''
        INSERT INTO nyc_weather_hourly (
            date, temperature_2m, relative_humidity_2m, dew_point_2m,
            apparent_temperature, precipitation, snowfall, pressure_msl,
            cloud_cover, wind_speed_10m, wind_direction_10m, wind_gusts_10m
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', row)

conn.commit()
conn.close()

print("Weather CSV imported")
