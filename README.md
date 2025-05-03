# CS381
Introduction to Machine Learning

## Goal
In this project, I use machine learning to accurately predict the energy consumption of New York City in MW at any given hour in the day, given the date and the weather conditions.

## To Run
Two files are needed to run the project: Final_Project.ipynb and nyc_energy_and_weather.db

1. Download those two files to the same directory within Google Drive.
2. Within Final_Project.ipynb, edit the third cell so that the path to the database that is being imported is the same was where the nyc_energy_and_weather.db that was just downloaded is stored
3. Select within the top bar "Runtime" --> then "Run all"
    - if google drives asks to "Permit this notebook to access your Google Drive files?," click "Connect to Google Drive" --> Choose the email account associated with the google drive that the above files were downloaded into --> Permit access
4. See the results of each cell, the final cell shows a summary of the best models, which model was the best of all (this being the final model that I chose for the project), and analysis of success.




## Files Within Directory
**Note: Do not run any of the code with the scripts directory. The results of the scripts are already stored within nyc_energy_and_weather.db, please use the results instead**

Within this directory is the code to create the database for predicting energy consumption of NYC at a given hour using the date, time and weather. 
- Final_Project.ipynb: Contains all of the machine learning code/scripts used for the project. Must import the nyc_energy_and_weather.db to create the model to predict the energy consumption of NYC in MW in a given hour, given the weather and date.
- nyc_energy_and_weather.db: database of just the final table (nyc_hourly_merged_added), this is what I turned in as it is much smaller in data than nyc.db
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
        - get_weather_data.py: gets the weather data from https://archive-api.open-meteo.com/v1/archive and stores the data in a csv
        - create_table.py: creates the nyc_weather_hourly table to take the data in the csv
        - csv_to_sqlite.py: copies the data from the csv into nyc_weather_hourly
        - clean_weather_table.py: creates features (hour, day_of_week, is_weekend, year, month, day, is_holiday)
