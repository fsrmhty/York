#York
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import socket
import platform

# Function to get the machine's IP address
def get_machine_ip():
    # Get the hostname
    hostname = socket.gethostname()
    # Get the IP address associated with the hostname
    ip_address = socket.gethostbyname(hostname)
    return ip_address

# Function to get the machine name
def get_machine_name():
    # Retrieve the node name of the local machine
    machine_name = platform.node()
    return machine_name

if __name__ == "__main__":
    # Print the machine's IP and name
    ip = get_machine_ip()
    name = get_machine_name()
    print(f"Machine IP: {ip}")
    print(f"Machine Name: {name}")
    print("my name is York")

    # Load income data from an Excel file and expenses data from a text file
    income_df = pd.read_excel('income2.xlsx')
    expenses_df = pd.read_csv('expenses2.txt', sep=' ')

    # Convert 'Month' columns in both dataframes to datetime format
    income_df['Month'] = pd.to_datetime(income_df['Month'].str.strip(), format='%Y-%m-%d', errors='coerce')
    expenses_df['Month'] = pd.to_datetime(expenses_df['Month'].str.strip(), format='%Y-%m-%d', errors='coerce')

    # Check for invalid dates and print warnings if any
    if income_df['Month'].isna().any():
        print("Warning: Invalid dates found in income data.")
    if expenses_df['Month'].isna().any():
        print("Warning: Invalid dates found in expenses data.")

    # Merge income and expenses dataframes on 'Month'
    merged_df = pd.merge(income_df, expenses_df, on='Month', how='inner')

    # Calculate savings by subtracting expenses from income
    merged_df['Savings'] = merged_df['Income'] - merged_df['Expenses']

    # Filter rows where income is greater than 7000 and savings are positive
    filtered_df = merged_df[(merged_df['Income'] > 7000) & (merged_df['Savings'] > 400)]
    filtered_df = filtered_df.sort_values(by='Month', ascending=True)

    # Select relevant columns for display
    filtered_df = filtered_df[['Month', 'Income', 'Expenses', 'Savings']]

    # Validate that total income is positive and expenses do not exceed income
    if merged_df['Income'].sum() <= 0:
        raise ValueError("Total income must be greater than zero.")
    if merged_df['Expenses'].sum() > merged_df['Income'].sum():
        raise ValueError("Total expenses cannot exceed total income.")

    # Calculate percentage of expenses vs total income
    expense_percentage = merged_df['Expenses'].sum() / merged_df['Income'].sum() * 100
    labels = ['Expenses', 'Savings']
    sizes = [max(0, expense_percentage), max(0, 100 - expense_percentage)]

    # Retrieve machine name and IP address
    machine_name= get_machine_name()
    ip_address= get_machine_ip()

    print(f"Machine name:{machine_name}")
    print(f"IP Adress:{ip_address}")

    # Save merged dataframe to SQLite database
    conn = sqlite3.connect('finance_data.db')
    merged_df.to_sql('FinanceData', conn, if_exists='replace', index=False)
    conn.close()

    # Plotting the data
    plt.figure(figsize=(12, 6))

    # Pie chart showing distribution between expenses and savings
    plt.subplot(1, 2, 1)
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title('Expense vs Savings Distribution')

    # Line chart showing monthly savings trends
    plt.subplot(1, 2, 2)
    merged_df.sort_values('Month', inplace=True)
    merged_df.set_index('Month')['Savings'].plot(kind='line', marker='o', color='green')
    plt.title('Monthly Savings Trends')
    plt.xlabel('Month')
    plt.ylabel('Savings ($)')

    # Add title with machine name and IP address at the bottom
    plt.suptitle(f"Machine Name: {machine_name}\nIP Address: {ip_address}", fontsize=10, y=0.02, ha='left', va='bottom')

    plt.tight_layout()
    plt.show()
