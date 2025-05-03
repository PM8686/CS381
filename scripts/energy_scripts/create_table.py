import sqlite3


# Create a connection to the SQLite database (it will create the database if it doesn't exist)
conn = sqlite3.connect('../nyc.db')
db = conn.cursor()

# Step 1: Create the database table
# Adjust the columns based on the structure of your CSV files
create_table_sql = '''
CREATE TABLE IF NOT EXISTS energy_data (
    "Time Stamp" TEXT,
    "Time Zone" TEXT,
    "Name" TEXT,
    "PTID" INTEGER,
    "Load" REAL
);
'''

# Execute the SQL command to create the table
db.execute(create_table_sql)
conn.commit()

# Close the connection after creating the table
conn.close()

print("energy_data table created")
