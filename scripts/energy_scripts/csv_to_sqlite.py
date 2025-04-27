import os
import sqlite3
import csv

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up one level
CSV_DIR = os.path.join(BASE_DIR, 'csvs') 
DB_PATH = os.path.join(BASE_DIR, 'nyc_energy.db')

# Create a connection to the SQLite database
conn = sqlite3.connect(DB_PATH)
db = conn.cursor()

# Step 2: Import CSV data into the database
for filename in os.listdir(CSV_DIR):
    if filename.endswith('.csv'):
        file_path = os.path.join(CSV_DIR, filename)

        print(f"Importing {filename}...")

        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)  # Skip the header row

            # Insert rows into the database
            for row in reader:
                db.execute('''
                INSERT INTO energy_data ("Time Stamp", "Time Zone", "Name", "PTID", "Load")
                VALUES (?, ?, ?, ?, ?)
                ''', (row[0], row[1], row[2], row[3], row[4]))

        # Commit the changes after each file
        conn.commit()

# Close the connection after all CSVs are processed
conn.close()

print("All CSV data imported successfully.")
