
import sqlite3


# Create a connection to the SQLite database (it will create the database if it doesn't exist)
conn = sqlite3.connect('../nyc.db')
db = conn.cursor()

# Step 1: Create the database table
# Adjust the columns based on the structure of your CSV files
create_table_sql = '''
CREATE TABLE IF NOT EXISTS nyc_weather_hourly (
    date TEXT,
    temperature_2m REAL,
    relative_humidity_2m REAL,
    dew_point_2m REAL,
    apparent_temperature REAL,
    precipitation REAL,
    snowfall REAL,
    pressure_msl REAL,
    cloud_cover REAL,
    wind_speed_10m REAL,
    wind_direction_10m REAL,
    wind_gusts_10m REAL
);
'''

# Execute the SQL command to create the table
db.execute(create_table_sql)
conn.commit()

# Close the connection after creating the table
conn.close()

print("Database and table created successfully.")



