import pandas as pd
import sqlite3

# loading cleaned data from csv file
orders_df = pd.read_csv('orders_clean.csv')
region_df = pd.read_csv('regions_master.csv')  

# connecting to SQLite database
conn = sqlite3.connect('pharmeasy.db')

# creating tables in the database
region_df.to_sql('region_master', conn, if_exists='replace', index=False)  # Create region_master table
orders_df.to_sql('orders_clean', conn, if_exists='replace', index=False)  # Create orders_clean table

# checking row counts in the tables
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM region_master")
region_count = cursor.fetchone()[0]
print(f"Row count in region_master: {region_count}")

cursor.execute("SELECT COUNT(*) FROM orders_clean")
orders_count = cursor.fetchone()[0]
print(f"Row count in orders_clean: {orders_count}")

conn.close()


