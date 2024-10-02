import pandas as pd
import os

# Load the daily returns data
daily_returns = pd.read_csv('djia_daily_returns.csv')
daily_returns['Date'] = pd.to_datetime(daily_returns['Date']).dt.date  # Ensure 'Date' is in datetime format

# Load the original stock data with adjusted close prices
stock_data = pd.read_csv('djia_all_data.csv')
stock_data['Date'] = pd.to_datetime(stock_data['Date']).dt.date # Ensure 'Date' is in datetime format

# Set the initial amount of money
initial_money = 100000
current_money = initial_money

# To store the money over time for the trading strategy
money_over_time = []

# Get a list of all unique dates
all_dates = sorted(daily_returns['Date'].unique())

# Simulate the trading strategy over the entire period
for i in range(len(all_dates) - 1):
    current_date = all_dates[i]
    next_date = all_dates[i + 1]

    # Find the 10 worst performing stocks on the current date
    daily_data = daily_returns[daily_returns['Date'] == current_date]
    worst_stocks = daily_data.nsmallest(10, 'Daily Return')

    # Calculate 5% of the current money for each stock
    investment_per_stock = 0.10 * current_money

    # Track total investment for the day
    total_investment = 0

    for _, stock in worst_stocks.iterrows():
        symbol = stock['Symbol']

        # Get the closing price of the current day
        current_day_price = stock_data[(stock_data['Date'] == current_date) & (stock_data['Symbol'] == symbol)]['Adj Close'].values
        if current_day_price.size == 0:
            print(f"Missing price data for {symbol} on {current_date}. Skipping trade.")
            continue

        current_day_price = current_day_price[0]

        # Check if there's enough money to invest
        if current_money < investment_per_stock:
            print(f"Not enough money to invest in {symbol} on {current_date}. Skipping trade.")
            continue

        # Calculate the number of shares to buy
        num_shares = investment_per_stock / current_day_price

        # Get the closing price of the next day
        next_day_price = stock_data[(stock_data['Date'] == next_date) & (stock_data['Symbol'] == symbol)]['Adj Close'].values
        if next_day_price.size == 0:
            print(f"Missing price data for {symbol} on {next_date}. Skipping sale.")
            continue

        next_day_price = next_day_price[0]

        # Calculate the money after selling at next day's price
        sale_amount = num_shares * next_day_price
        profit_loss = sale_amount - investment_per_stock

        # Update the current money
        current_money += profit_loss
        total_investment += investment_per_stock

    # Record the current money and date
    money_over_time.append({'Date': next_date, 'Money': current_money, 'Strategy': 'WorstPerDay'})

    # Print the money after each day's trading
    print(f"Date: {next_date.strftime('%Y-%m-%d')}, Money: ${current_money:,.2f}")

# Create a DataFrame to store the new Trading strategy results
money_df = pd.DataFrame(money_over_time)

# Check if the shared CSV file exists
csv_file = 'strategy_comparison.csv'
if os.path.isfile(csv_file):
    # Load the existing CSV file
    existing_data = pd.read_csv(csv_file)

    # Remove any previous Trading strategy data
    existing_data = existing_data[existing_data['Strategy'] != 'WorstPerDay']

    # Append the new Trading strategy data to the existing data
    combined_data = pd.concat([existing_data, money_df], ignore_index=True)
else:
    # If no file exists, use only the new Trading strategy data
    combined_data = money_df

# Save the updated data to the CSV file, overwriting only the relevant strategy section
combined_data.to_csv(csv_file, index=False)
print("Trading strategy results updated in 'strategy_comparison.csv'.")
