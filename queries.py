import sqlite3
import pandas as pd

conn = sqlite3.connect('pharmeasy.db')

print("Checking row counts in the tables...")

left_join_query = """
SELECT COUNT(*) AS left_join_count
FROM region_master r
LEFT JOIN orders_clean o ON r.region = o.region
"""

iner_join_query = """
SELECT COUNT(*) AS inner_join_count
FROM region_master r
INNER JOIN orders_clean o ON r.region = o.region
"""
left_count = pd.read_sql_query(left_join_query, conn).iloc[0]['left_join_count']
inner_count = pd.read_sql_query(iner_join_query, conn).iloc[0]['inner_join_count']  

print(f"Row count after LEFT JOIN: {left_count}")
print(f"Row count after INNER JOIN: {inner_count}") 

# checking for dup order id 

print("Checking for duplicate order IDs in orders_clean table...")
duplicate_query = """   
SELECT order_id, COUNT(*) AS count
FROM orders_clean   
GROUP BY order_id
HAVING COUNT(*) > 1
"""
duplicate_orders = pd.read_sql_query(duplicate_query, conn)

if not duplicate_orders.empty:
    print("Duplicate order IDs found:")
    print(duplicate_orders)
else:
    print("No duplicate order IDs found.")


count_query  = """
SELECT r.region, Count(*) As count_star,
Count(o.order_id) As count_order_id
FROM region_master r
LEFT JOIN orders_clean o ON r.region = o.region
GROUP BY r.region
ORDER BY r.region
"""

count_comparison = pd.read_sql_query(count_query, conn)
print("Count comparison between region_master and orders_clean:")   
print(count_comparison)

# Regions where counts do not match

disagreement = count_comparison[count_comparison['count_star'] != count_comparison['count_order_id']]
if not disagreement.empty:
    print("Regions where counts do not match:")
    print(disagreement) 

# count region wise

print("Counting orders region-wise...")
region_count_query = """
SELECT r.region, COUNT(o.order_id) AS order_count
FROM region_master r
LEFT JOIN orders_clean o ON r.region = o.region
GROUP BY r.region
ORDER BY order_count ASC

"""
region_counts = pd.read_sql_query(region_count_query, conn) 
print("Region-wise order counts:")
print(region_counts)

# monthly sales region wise

monthly_sales_query = """
SELECT region, substr(order_date, 1, 7) AS month, ROUND(SUM(sales_inr),2) AS total_sales
FROM orders_clean
GROUP BY region, month
ORDER BY region, month

"""

monthly_sales = pd.read_sql_query(monthly_sales_query, conn)
print("Monthly sales region-wise:") 
print(monthly_sales)


# saving the results into tables in the database

sales_pivot=monthly_sales.pivot(index='region', columns='month', values='total_sales')

print("Saving the results into tables in the database...")
print(sales_pivot)

sales_pivot.to_csv("region_month_sales.csv")

conn.close()


