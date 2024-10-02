# Backtester


## Stock Trading Strategy Backtesting Suite

This backtesting suite is a flexible and comprehensive tool designed to evaluate different stock trading strategies using historical data. It enables users to simulate the performance of various strategies, compare results, and analyze risk and return metrics. By utilizing this backtesting suite, users can make informed decisions about the effectiveness of different trading strategies before deploying them in live markets.

If you want to learn more about the process read below!

### Key Features:
- **Pre-processing Automation**: Automates the process of fetching and calculating necessary stock data, including adjusted close prices and daily returns, for use in strategy simulations.
  
- **Multiple Strategy Support**: The suite supports several trading strategies, including:
  - **Worst Per Day**: Invests in the 10 worst-performing stocks based on daily returns, aiming to capitalize on potential price rebounds.
  - **Buy and Hold**: Divides capital equally among all stocks and holds them for the entire duration, providing a baseline for performance comparison.
  - **Mean Reversion**: Identifies stocks that have deviated from their historical averages, expecting prices to revert back to the mean.
  - **Reversal Strategy**: Detects underperforming stocks compared to their moving average, investing in them with the expectation of a price reversal back to historical levels.

- **User-Selectable Strategies**: The suite allows users to select which strategies to run, enabling side-by-side comparison of multiple strategies within the same market period.
  
- **Post-Processing and Analysis**: After running the selected strategies, the suite includes performance analysis tools that provide key insights into the performance of each strategy, including total returns, risk, and volatility.

### Workflow:
1. **Data Fetching**: The suite fetches stock price data and calculates daily returns for each stock, ensuring that all necessary data is prepared for strategy execution.
  
2. **Strategy Selection**: Users can select multiple strategies to test, either individually or in combination, providing flexibility in how strategies are evaluated.

3. **Backtesting Execution**: The suite simulates the strategies over the selected time period, updating the portfolio based on the rules defined for each strategy.

4. **Performance Analysis**: Once the strategies are executed, the software performs a detailed analysis of each strategy's performance, helping users understand the strengths and weaknesses of each approach.

### How to Use:
1. Clone the repository.
2. Install the required dependencies listed in `requirements.txt`.
3. Run the main script (`MainScript.py`), which will guide you through the selection of strategies and automatically execute the backtest.
4. View the performance summary and analysis provided at the end of the run.

