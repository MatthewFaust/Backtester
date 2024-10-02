import pandas as pd
import os

# Load the original stock data with adjusted close prices
stock_data = pd.read_csv('djia_all_data.csv')
stock_data['Date'] = pd.to_datetime(stock_data['Date'])  # Ensure 'Date' is in datetime format

# Set parameters for the strategy
lookback_period = 20  # Look back 20 days for mean reversion
reversal_threshold = 0.05  # A reversal occurs if the stock is underperforming its moving average by more than 5%
initial_money = 100000
current_money = initial_money

# To store the money over time for the trading strategy
money_over_time = []

# Get a list of all unique symbols
all_symbols = stock_data['Symbol'].unique()

# Get a list of all unique dates
all_dates = sorted(stock_data['Date'].unique())

# Simulate the trading strategy over the entire period
for i in range(lookback_period, len(all_dates) - 1):
    current_date = all_dates[i]
    next_date = all_dates[i + 1]

    # Track total investment for the day
    total_investment = 0

    for symbol in all_symbols:
        symbol_data = stock_data[stock_data['Symbol'] == symbol]

        # Ensure there's enough data for the lookback period
        if len(symbol_data[symbol_data['Date'] <= current_date]) < lookback_period:
            continue

        # Calculate the moving average of the last 'lookback_period' days
        recent_data = symbol_data[symbol_data['Date'] <= current_date].tail(lookback_period)
        moving_average = recent_data['Adj Close'].mean()

        # Get the current day's adjusted close price
        current_day_price = symbol_data[symbol_data['Date'] == current_date]['Adj Close'].values
        if current_day_price.size == 0:
            print(f"Missing price data for {symbol} on {current_date}. Skipping trade.")
            continue
        current_day_price = current_day_price[0]

        # Check if the stock price is underperforming the moving average by more than the threshold
        if current_day_price < moving_average * (1 - reversal_threshold):
            # Calculate 10% of the current money for this stock
            investment_per_stock = 0.10 * current_money

            # Calculate the number of shares to buy
            num_shares = investment_per_stock / current_day_price

            # Get the next day's adjusted close price for selling
            next_day_price = symbol_data[symbol_data['Date'] == next_date]['Adj Close'].values
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
    money_over_time.append({'Date': next_date, 'Money': current_money, 'Strategy': 'Reversal'})

    # Print the money after each day's trading
    print(f"Date: {next_date.strftime('%Y-%m-%d')}, Money: ${current_money:,.2f}")

# Create a DataFrame to store the new Reversal strategy results
money_df = pd.DataFrame(money_over_time)

# Convert 'Date' to string in YYYY-MM-DD format before saving
money_df['Date'] = pd.to_datetime(money_df['Date']).dt.strftime('%Y-%m-%d')

# Check if the shared CSV file exists
csv_file = 'strategy_comparison.csv'
if os.path.isfile(csv_file):
    # Load the existing CSV file
    existing_data = pd.read_csv(csv_file)

    # Remove any previous Reversal strategy data
    existing_data = existing_data[existing_data['Strategy'] != 'Reversal']

    # Append the new Reversal strategy data to the existing data
    combined_data = pd.concat([existing_data, money_df], ignore_index=True)
else:
    # If no file exists, use only the new Reversal strategy data
    combined_data = money_df

# Save the updated data to the CSV file, ensuring the 'Date' column has no time component
combined_data.to_csv(csv_file, index=False)
print("Reversal strategy results updated in 'strategy_comparison.csv'.")
