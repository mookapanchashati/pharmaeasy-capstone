import pandas as pd


df = pd.read_csv("pharmeasy_orders_raw.csv ") # Load the raw data from CSV file
print("Raw data shape:", df.shape)
before = len(df) # before cleaning count of rows
print("Raw data total rows:", before)

df = df.drop_duplicates() # Remove duplicate rows

duplicate_rows = df[df.duplicated()]

duplicates_removed = before - len(df) # Count of duplicates removed
print("Duplicates removed:", duplicates_removed)
print("Cleaned data shape:", df.shape)
print("Rows after cleaning:", len(df)) # After deduplication count of rows

df["region"] = df["region"].str.strip().str.title() # Remove leading and trailing spaces from the 'region' column

print("Regions")
print(sorted(df["region"].unique())) # Print unique values in the 'region' column
