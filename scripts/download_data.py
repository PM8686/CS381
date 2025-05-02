import sqlite3

# Connect to original and new database
conn_orig = sqlite3.connect("../nyc.db")
conn_new = sqlite3.connect("../nyc_energy_and_weather.db")

table_name = "nyc_hourly_merged_added"

# Copy the table schema and create the table in the new database
create_stmt = conn_orig.execute(
    f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}'"
).fetchone()[0]
conn_new.execute(create_stmt)

# Copy all data
rows = conn_orig.execute(f"SELECT * FROM {table_name}").fetchall()
conn_new.executemany(
    f"INSERT INTO {table_name} VALUES ({','.join(['?'] * len(rows[0]))})", rows
)

# Commit and close
conn_new.commit()
conn_orig.close()
conn_new.close()

print("Exported table to new database:", "nyc_energy_and_weather.db")
