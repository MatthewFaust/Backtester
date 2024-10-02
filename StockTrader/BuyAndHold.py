import pandas as pd
import os

# Load the original stock data with adjusted close prices
stock_data = pd.read_csv('djia_all_data.csv')
stock_data['Date'] = pd.to_datetime(stock_data['Date']).dt.date  # Ensure 'Date' is in datetime format

# Set initial money for equal investment strategy
initial_money = 100000
equal_investment_money = initial_money

# Get unique symbols of all stocks in the dataset
all_symbols = stock_data['Symbol'].unique()

# Dictionary to track shares owned for each stock
shares_owned = {}

# Calculate the investment per stock
investment_per_stock = equal_investment_money / len(all_symbols)

# Get the list of all unique dates
all_dates = sorted(stock_data['Date'].unique())

# Start date (10 years ago)
start_date = all_dates[0]

# Invest equally in all stocks
for symbol in all_symbols:
    # Get the first available date for the stock
    first_available_date = stock_data[stock_data['Symbol'] == symbol]['Date'].min()
    first_day_price = stock_data[(stock_data['Date'] == first_available_date) & (stock_data['Symbol'] == symbol)]['Adj Close'].values

    if first_day_price.size == 0:
        print(f"Missing price data for {symbol} on its first available date. Skipping initial investment.")
        continue

    first_day_price = first_day_price[0]
    num_shares = investment_per_stock / first_day_price
    shares_owned[symbol] = num_shares

# To store the money over time for buy-and-hold strategy
money_over_time = [{'Date': start_date, 'Money': equal_investment_money, 'Strategy': 'Buy-and-Hold'}]

# Calculate the value of the portfolio for each day
for current_date in all_dates:
    # Calculate the total value of the portfolio on the current date
    total_value = 0
    for symbol, shares in shares_owned.items():
        # Get the current day's adjusted close price for each stock
        current_day_price = stock_data[(stock_data['Date'] == current_date) & (stock_data['Symbol'] == symbol)]['Adj Close'].values
        if current_day_price.size == 0:
            print(f"Missing price data for {symbol} on {current_date}. Skipping value calculation for this stock.")
            continue

        current_day_price = current_day_price[0]
        total_value += shares * current_day_price

    # Update the total money
    equal_investment_money = total_value

    # Record the current money and date
    money_over_time.append({'Date': current_date, 'Money': equal_investment_money, 'Strategy': 'Buy-and-Hold'})

    # Print the money after each day's value update
    print(f"Date: {current_date.strftime('%Y-%m-%d')}, Money: ${equal_investment_money:,.2f}")

# Create a DataFrame to store the new Buy-and-Hold strategy results
money_df = pd.DataFrame(money_over_time)

# Check if the shared CSV file exists
csv_file = 'strategy_comparison.csv'
if os.path.isfile(csv_file):
    # Load the existing CSV file
    existing_data = pd.read_csv(csv_file)

    # Remove any previous Buy-and-Hold strategy data
    existing_data = existing_data[existing_data['Strategy'] != 'Buy-and-Hold']

    # Append the new Buy-and-Hold strategy data to the existing data
    combined_data = pd.concat([existing_data, money_df], ignore_index=True)
else:
    # If no file exists, use only the new Buy-and-Hold strategy data
    combined_data = money_df

# Save the updated data to the CSV file, overwriting only the relevant strategy section
combined_data.to_csv(csv_file, index=False)
print("Buy-and-Hold strategy results updated in 'strategy_comparison.csv'.")
