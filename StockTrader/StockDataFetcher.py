import pandas as pd
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime, timedelta

# Step 1: Fetch DJIA constituents from Wikipedia
wiki_url = "https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average"
response = requests.get(wiki_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the table with DJIA constituents
table = soup.find('table', {'class': 'wikitable'})

# Parse the table to get stock symbols and company names
djia_data = []
for row in table.find_all('tr')[1:]:
    columns = row.find_all('td')
    if columns:
        symbol = columns[1].text.strip()
        company_name = columns[0].text.strip()
        djia_data.append({'Symbol': symbol, 'Company': company_name})

# Convert to DataFrame and save to CSV
djia_df = pd.DataFrame(djia_data)
djia_df.to_csv('djia_constituents.csv', index=False)
print("DJIA constituents saved to 'djia_constituents.csv'.")

# Step 2 & 3: Fetch 10 years of daily adjusted close prices and save to CSV
end_date = datetime.today().strftime('%Y-%m-%d')  # Today’s date in 'YYYY-MM-DD' format
start_date = (datetime.today() - timedelta(days=365*10)).strftime('%Y-%m-%d')  # 10 years ago
data_dir = "djia_stock_data"
os.makedirs(data_dir, exist_ok=True)

for index, row in djia_df.iterrows():
    symbol = row['Symbol']
    company = row['Company']
    try:
        # Download stock data using yfinance
        stock_data = yf.download(symbol, start=start_date, end=end_date)

        # Explicitly add the 'Date' column from the index
        stock_data['Date'] = stock_data.index

        # Add company and symbol columns
        stock_data['Company'] = company
        stock_data['Symbol'] = symbol

        # Save the data to a CSV file
        stock_data.to_csv(f'{data_dir}/{symbol}.csv', index=False)  # Overwrite each file
        print(f"Data for {symbol} saved successfully.")
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")

# Step 4: Load the constituent symbols and price data from the CSV files
all_data = pd.DataFrame()

for index, row in djia_df.iterrows():
    symbol = row['Symbol']
    company = row['Company']
    try:
        stock_df = pd.read_csv(f'{data_dir}/{symbol}.csv', parse_dates=['Date'])  # Ensure 'Date' is parsed as datetime
        stock_df['Company'] = company  # Add company name column if missing
        stock_df['Symbol'] = symbol  # Add symbol column if missing
        all_data = pd.concat([all_data, stock_df], axis=0)  # Combine all data
    except FileNotFoundError:
        print(f"Data file for {symbol} not found.")
    except Exception as e:
        print(f"Error processing data for {symbol}: {e}")

# Step 5: Handle missing data using forward fill
all_data = all_data.groupby('Symbol').apply(lambda x: x.fillna(method='ffill')).reset_index(drop=True)

# Save the combined data to a CSV file (overwrite by default)
all_data.to_csv('djia_all_data.csv', index=False)
print("All DJIA data saved to 'djia_all_data.csv'.")
