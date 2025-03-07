import pandas as pd
import sqlite3

# Extract: Read data from a CSV file
customers_df = pd.read_csv('customer.csv')
orders_df = pd.read_csv('orders.csv')

# Transform: Data Transformation
# Merge data
merged_df = pd.merge(orders_df, customers_df, on='CustomerID', how='inner')

# Calculate the total amount
merged_df['TotalAmount'] = merged_df['Quantity'] * merged_df['Price']

# Add a status column
merged_df['Status'] = merged_df['OrderDate'].apply(lambda d: 'New' if d.startswith('2025-03') else 'Old')

# Filter high-value orders
high_value_orders = merged_df[merged_df['TotalAmount'] > 5000]

# Load: Data load
# Connect to the database
conn = sqlite3.connect('ecommerce.db')

# Create a table
create_table_query = '''
CREATE TABLE IF NOT EXISTS HighValueOrders (
    OrderID INTEGER,
    CustomerID INTEGER,
    Name TEXT,
    Email TEXT,
    Product TEXT,
    Quantity INTEGER,
    Price REAL,
    OrderDate TEXT,
    TotalAmount REAL,
    Status TEXT
)
'''
conn.execute(create_table_query)

# Load the data
high_value_orders.to_sql('HighValueOrders', conn, if_exists='replace', index=False)

# Validate the data
result = conn.execute('SELECT * FROM HighValueOrders')
for row in result.fetchall():
    print(row)

# Close the connection
conn.close()

print("ETL process completed successfully!")
