import subprocess

# List of pre-processing scripts (always run before the strategies)
pre_processing_scripts = [
    {"file": "StockDataFetcher.py", "description": "Fetch stock data"},
    {"file": "FindDailyReturns.py", "description": "Calculate daily returns"}
]

# List of strategy scripts (user selects which ones to run)
strategies = {
    1: {"file": "WorstPerDaySim.py", "description": "WorstPerDay -- The **Worst Per Day Strategy** involves identifying the 10 worst-performing stocks from the previous trading day \n"
                                                    "(based on daily returns) and investing a portion of the available capital in each of them. The goal is to capitalize on potential \n"
                                                    "price rebounds by buying stocks that performed poorly and selling them after one day. This strategy aims to take advantage of market \n"
                                                    "corrections or short-term recoveries in underperforming stocks.\n"},
    2: {"file": "BuyAndHold.py", "description": "BuyAndHold -- Divides capital equally among all stocks in the S&P 500\n"},
    3: {"file": "MeanReversionSim.py", "description": "MeanReversion -- The Mean Reversion Strategy identifies stocks that have deviated significantly from their historical averages (e.g., moving averages) \n"
                                                      "and trades them with the expectation that their prices will revert to the mean. The strategy buys stocks that are underperforming \n"
                                                      "relative to their historical averages, expecting a price recovery. \n"},
    4: {"file": "Reversal.py", "description": "Reversal -- The Reversal Strategy buys stocks that are underperforming compared to their moving average by a certain threshold, expecting a reversal \n"
                                                      "back to the average price. It looks for opportunities where stocks have dropped significantly and may rise back to their historical price levels.\n"}
}

# List of post-processing scripts (always run after the strategies)
post_processing_scripts = [
    {"file": "PerformanceAnalyzer.py", "description": "Analyze and compare strategy performance"}
]

# Function to run a script
def run_script(script_file):
    try:
        print(f"Running {script_file}...")
        result = subprocess.run(['python', script_file], check=True)
        print(f"{script_file} completed successfully.\n")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_file}: {e}")
        return False
    return True

# Step 1: Run pre-processing scripts
print("Starting pre-processing steps...\n")
for script in pre_processing_scripts:
    if not run_script(script["file"]):
        print(f"Failed to complete pre-processing step: {script['file']}. Exiting.")
        exit(1)

# Step 2: Prompt user to select strategies
print("Strategy Descriptions:")
for key, strategy in strategies.items():
    print(f"{key}. {strategy['description']}")

# Get user input for strategies
print("Enter the numbers of the strategies you want to run separated by a comma: ")
selected_strategies = input("For example, 1,2 would run WorstPerDay and BuyAndHold. It is recommended you run BuyAndHold as a baseline.\n").split(',')
selected_strategies = [int(num.strip()) for num in selected_strategies if num.strip().isdigit() and int(num.strip()) in strategies]

if not selected_strategies:
    print("No valid strategies selected. Exiting.")
    exit(0)

# Step 3: Run the selected strategy scripts
for strategy_num in selected_strategies:
    strategy = strategies[strategy_num]
    if not run_script(strategy["file"]):
        print(f"Failed to complete strategy step: {strategy['file']}. Exiting.")
        exit(1)

# Step 4: Run post-processing scripts (e.g., Performance Analyzer)
print("Starting post-processing steps...\n")
for script in post_processing_scripts:
    if not run_script(script["file"]):
        print(f"Failed to complete post-processing step: {script['file']}. Exiting.")
        exit(1)

print("All steps completed successfully.")
