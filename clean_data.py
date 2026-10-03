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

# Missing categories

product_category = (df.dropna(subset = ["category"])
                    .drop_duplicates(subset = ["product"])
                    .set_index("product")["category"].to_dict()) # Create a dictionary mapping products to their categories 

df["category"] = df["category"].fillna(df["product"].map(product_category)) # Fill missing categories based on the product mapping  

print("Missing categories filled based on product mapping.", df["category"].isna().sum())

# Profit calculation

df["profit_margin"] = df["profit_inr"] / df["sales_inr"] # Calculate profit margin as profit divided by sales

category_margins = (
    df.groupby("category")["profit_margin"]
    .mean()
)

missing_profit = df["profit_inr"].isna()

df.loc[missing_profit, "profit_inr"] = df.loc[missing_profit, "sales_inr"]* df.loc[missing_profit, "category"].map(category_margins).round(2) # Fill missing profit margins based on category averages

df = df.drop(columns=["profit_margin"]) # Drop the 'profit_margin' column as it is no longer needed

print("Missing profit margins filled based on category averages.", df["profit_inr"].isna().sum())


def validate_schema(df, required_columns):
    """
    Validate that the DataFrame contains all required columns.

    Parameters:
    df (pd.DataFrame): The DataFrame to validate.
    required_columns (list): A list of required column names.

    Returns:
    bool: True if all required columns are present, False otherwise.
    """
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"Missing columns: {missing_columns}")
        status = "Blocked Schema"
    else:
        status = "Schema Validated"

    return {
        "status": status,
        "row_count": len(df),
        "missing_columns": missing_columns
    }

required_columns = ["order_id", "order_date", "region", "category", "product", "quantity", "sales_inr", "profit_inr"]

result = validate_schema(df, required_columns)

print("valid schema:", result["status"])

# Negative test

broken_df = df.drop(columns=["profit_inr"])  # Create a broken DataFrame by dropping a required column    

broken_result = validate_schema(broken_df, required_columns)

# finally saving the dataset

df.to_csv("orders_clean.csv", index=False) # Save the cleaned DataFrame to a new CSV file

print("Cleaned data saved to 'orders_clean.csv'.")
