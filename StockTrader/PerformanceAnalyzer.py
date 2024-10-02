import pandas as pd
import numpy as np

# Load the strategy comparison data
data = pd.read_csv('strategy_comparison.csv')
data['Date'] = pd.to_datetime(data['Date'])  # Ensure 'Date' is in datetime format

# Calculate daily returns for each strategy
data['Daily Return'] = data.groupby('Strategy')['Money'].pct_change()

# Annualization factor assuming 252 trading days in a year
annualization_factor = 252

# Initialize a dictionary to store the results
strategy_metrics = {}

# Calculate metrics for each strategy
for strategy in data['Strategy'].unique():
    strategy_data = data[data['Strategy'] == strategy].copy()
    strategy_data.set_index('Date', inplace=True)

    # Calculate annualized return
    total_return = (strategy_data['Money'].iloc[-1] / strategy_data['Money'].iloc[0]) - 1
    num_years = (strategy_data.index[-1] - strategy_data.index[0]).days / 365.25
    annualized_return = (1 + total_return) ** (1 / num_years) - 1

    # Calculate annualized volatility
    daily_volatility = strategy_data['Daily Return'].std()
    annualized_volatility = daily_volatility * np.sqrt(annualization_factor)

    # Calculate Sharpe ratio (assuming risk-free rate of 0)
    sharpe_ratio = annualized_return / annualized_volatility if annualized_volatility != 0 else np.nan

    # Store the results
    strategy_metrics[strategy] = {
        'Annualized Return': annualized_return,
        'Annualized Volatility': annualized_volatility,
        'Sharpe Ratio': sharpe_ratio,
    }

# Display the results
metrics_df = pd.DataFrame(strategy_metrics).T
print("Performance Metrics for Each Strategy:")
print(metrics_df)

# Save the results to a CSV file
metrics_df.to_csv('strategy_performance_metrics.csv', index=False)
print("Performance metrics saved to 'strategy_performance_metrics.csv'.")
