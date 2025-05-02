# CS381
Introduction to Machine Learning

Within this directory is the code to create the database for predicting energy consumption of NYC at a given hour using the date, time and weather. 
- scripts: contains all of the functions used to download the data form the internet, organize the data, and add more features
    - add_features.py: adds lag features and season feature to the whole dataset 
    - combine_tables.py: mergest nyc_weather_hourly_cleaned and nyc_energy_hourly_cleaned data after they have been cleaned
    - download_data.py: saves the final table into its own database so that is easier to download
    - energy_scripts: contains all scripts on just the energy data
        - get_energy_data.py: downloads nyc energy consumption data from "https://mis.nyiso.com/public/P-58Blist.htm" and stores it in csv files
        - create_table.py: creates the energy_data table to store the data from the above link
        - csv_to_sqlite.py: combines all of teh csv files into one sqlite table (energy_data)
        - clean_energy_table: creates features (hour, day_of_week, is_weekend, year, month, day, is_holiday), and it averages the load to the hour (flooring the minutes to the lower hour) and combines the samples that are within the same hour
    - weather_scriptsL contains all scripts on just the weather data
        - get_weather_data.py: gets the weather data from https://archive-api.open-meteo.com/v1/archive" and stores the data in a csv
        - create_table.py: creates the nyc_weather_hourly table to take the data in the csv
        - csv_to_sqlite.py: copies the data from the csv into nyc_weather_hourly
        - clean_weather_table.py: creates features (hour, day_of_week, is_weekend, year, month, day, is_holiday)
- nyc.db: contains all of the tables created by the above scripts (energy_data, nyc_hourly_merged, nyc_energy, nyc_hourly_merged_added, nyc_energy_cleaned, nyc_weather_hourly, nyc_energy_hourly_cleaned, nyc_weather_hourly_cleaned)
- nyc_energy_and_weather.db: database of just the final table (nyc_hourly_merged_added), this is what I turned in as it is much smaller in data than nyc.db
- 