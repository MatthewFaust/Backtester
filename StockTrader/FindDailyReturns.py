import pandas as pd

# Load the cleaned data from CSV into the DataFrame
data_filled = pd.read_csv('djia_all_data.csv')

# Check if 'Date' column exists, and if not, identify the correct column name
if 'Date' not in data_filled.columns:
    print("The 'Date' column is missing. Check for an alternative column name or ensure the data source is correct.")
else:
    # Convert 'Date' to datetime if it exists
    data_filled['Date'] = pd.to_datetime(data_filled['Date'])
    print("Date column successfully converted to datetime.")

# Function to calculate daily returns
def calculate_daily_returns(df):
    df['Daily Return'] = df['Adj Close'].pct_change()
    return df

# Check if 'Adj Close' column exists before proceeding
if 'Adj Close' not in data_filled.columns:
    print("The 'Adj Close' column is missing. Cannot calculate daily returns.")
else:
    # Group by 'Symbol' and apply the daily returns calculation
    data_filled = data_filled.groupby('Symbol').apply(calculate_daily_returns)

    # Drop the rows with NaN values in 'Daily Return' column which occur due to pct_change()
    data_filled.dropna(subset=['Daily Return'], inplace=True)

    # Display the DataFrame with daily returns calculated
    data_filled.reset_index(drop=True, inplace=True)

    # Save the DataFrame with daily returns to a new CSV file (overwrite the existing file)
    data_filled.to_csv('djia_daily_returns.csv', index=False)
    print("Daily returns saved to 'djia_daily_returns.csv'.")
