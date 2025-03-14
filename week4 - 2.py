import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import socket
import platform

def get_machine_ip():
    # Get the hostname
    hostname = socket.gethostname()
    # Get the IP address
    ip_address = socket.gethostbyname(hostname)
    return ip_address

def get_machine_name():
    # Get the machine name using platform
    machine_name = platform.node()
    return machine_name

if __name__ == "__main__":
    ip = get_machine_ip()
    name = get_machine_name()
    print(f"Machine IP: {ip}")
    print(f"Machine Name: {name}")
    print("my name is York")


income_df = pd.read_excel('income2.xlsx')
expenses_df = pd.read_csv('expenses2.txt', sep=' ')


income_df['Month'] = pd.to_datetime(income_df['Month'].str.strip(), format='%Y-%m-%d', errors='coerce')
expenses_df['Month'] = pd.to_datetime(expenses_df['Month'].str.strip(), format='%Y-%m-%d', errors='coerce')


if income_df['Month'].isna().any():
    print("Warning: Invalid dates found in income data.")
if expenses_df['Month'].isna().any():
    print("Warning: Invalid dates found in expenses data.")


merged_df = pd.merge(income_df, expenses_df, on='Month', how='inner')


merged_df['Savings'] = merged_df['Income'] - merged_df['Expenses']

filtered_df = merged_df[(merged_df['Income'] > 7000) & (merged_df['Savings'] > 400)]

filtered_df = filtered_df.sort_values(by='Month', ascending=True)

filtered_df = filtered_df[['Month', 'Income', 'Expenses', 'Savings']]

if merged_df['Income'].sum() <= 0:
    raise ValueError("Total income must be greater than zero.")
if merged_df['Expenses'].sum() > merged_df['Income'].sum():
    raise ValueError("Total expenses cannot exceed total income.")


expense_percentage = merged_df['Expenses'].sum() / merged_df['Income'].sum() * 100
labels = ['Expenses', 'Savings']
sizes = [max(0, expense_percentage), max(0, 100 - expense_percentage)]

machine_name= get_machine_name()
ip_address= get_machine_ip()

print(f"Machine name:{machine_name}")
print(f"IP Adress:{ip_address}")

conn = sqlite3.connect('finance_data.db')
merged_df.to_sql('FinanceData', conn, if_exists='replace', index=False)
conn.close()

query = """SELECT
  Month, Income, Expenses, Savings
FROM
    result table
WHERE
  Income > 7000 AND Savings > 400
ORDER BY
  Month ASC;"""


plt.figure(figsize=(12, 6))


plt.subplot(1, 2, 1)
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
plt.title('Expense vs Savings Distribution')


plt.subplot(1, 2, 2)
merged_df.sort_values('Month', inplace=True)
merged_df.set_index('Month')['Savings'].plot(kind='line', marker='o', color='green')
plt.title('Monthly Savings Trends')
plt.xlabel('Month')
plt.ylabel('Savings ($)')

plt.suptitle(f"Machine Name: {machine_name}\nIP Address: {ip_address}", fontsize=10, y=0.02, ha='left', va='bottom')

plt.tight_layout()
plt.show()