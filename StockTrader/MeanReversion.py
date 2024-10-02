import pandas as pd
import os

# Load the daily returns data
stock_data = pd.read_csv('djia_all_data.csv')
stock_data['Date'] = pd.to_datetime(stock_data['Date'])  # Ensure 'Date' is in datetime format

# Set parameters for the strategy
lookback_period = 50  # 50-day moving average
deviation_threshold = 0.05  # 5% deviation from the mean
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
        # Get the stock data for the current symbol
        symbol_data = stock_data[stock_data['Symbol'] == symbol]

        # Ensure there's enough data for the lookback period
        if len(symbol_data[symbol_data['Date'] <= current_date]) < lookback_period:
            continue

        # Calculate the rolling mean for the last 'lookback_period' days
        recent_data = symbol_data[symbol_data['Date'] <= current_date].tail(lookback_period)
        rolling_mean = recent_data['Adj Close'].mean()

        # Get the closing price of the current day
        current_day_price = symbol_data[symbol_data['Date'] == current_date]['Adj Close'].values
        if current_day_price.size == 0:
            continue
        current_day_price = current_day_price[0]

        # Check if the stock's price has deviated by more than the threshold from the mean
        if abs(current_day_price - rolling_mean) / rolling_mean > deviation_threshold:
            if current_day_price < rolling_mean:  # Stock is below its mean (buy signal)
                investment_per_stock = 0.10 * current_money  # Invest 10% of current money
                num_shares = investment_per_stock / current_day_price

                # Get the closing price of the next day
                next_day_price = symbol_data[symbol_data['Date'] == next_date]['Adj Close'].values
                if next_day_price.size == 0:
                    continue
                next_day_price = next_day_price[0]

                # Calculate the money after selling at the next day's price
                sale_amount = num_shares * next_day_price
                profit_loss = sale_amount - investment_per_stock

                # Update the current money
                current_money += profit_loss
                total_investment += investment_per_stock

    # Record the current money and date
    money_over_time.append({'Date': next_date, 'Money': current_money, 'Strategy': 'MeanReversion'})

    # Print the money after each day's trading
    print(f"Date: {next_date.strftime('%Y-%m-%d')}, Money: ${current_money:,.2f}")

# Create a DataFrame to store the new Mean Reversion strategy results
money_df = pd.DataFrame(money_over_time)

# Convert 'Date' to string in YYYY-MM-DD format before saving
money_df['Date'] = pd.to_datetime(money_df['Date']).dt.strftime('%Y-%m-%d')

# Check if the shared CSV file exists
csv_file = 'strategy_comparison.csv'
if os.path.isfile(csv_file):
    # Load the existing CSV file
    existing_data = pd.read_csv(csv_file)

    # Remove any previous Mean Reversion strategy data
    existing_data = existing_data[existing_data['Strategy'] != 'MeanReversion']

    # Append the new Mean Reversion strategy data to the existing data
    combined_data = pd.concat([existing_data, money_df], ignore_index=True)
else:
    # If no file exists, use only the new Mean Reversion strategy data
    combined_data = money_df

# Save the updated data to the CSV file, ensuring the 'Date' column has no time component
combined_data.to_csv(csv_file, index=False)
print("Mean Reversion strategy results updated in 'strategy_comparison.csv'.")
