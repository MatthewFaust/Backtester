import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Load the strategy comparison data
data = pd.read_csv('strategy_comparison.csv')
data['Date'] = pd.to_datetime(data['Date'])  # Ensure 'Date' is in datetime format

# Get all unique strategies present in the data
strategies = data['Strategy'].unique()

# Initialize an empty dictionary to store data for each strategy
strategy_data = {}

# Loop through each strategy and extract its data
for strategy in strategies:
    strategy_data[strategy] = data[data['Strategy'] == strategy]

# Create the figure
fig = make_subplots()

# Add traces for each strategy dynamically
for strategy, df in strategy_data.items():
    trace = go.Scatter(
        x=df['Date'],
        y=df['Money'],
        mode='lines',
        name=f'{strategy} Strategy',
        hoverinfo='text',
        text=[f'Date: {date}<br>Money: ${money:,.2f}' for date, money in zip(df['Date'], df['Money'])]
    )
    fig.add_trace(trace)

# Find the maximum value reached by any strategy
max_value = max([df['Money'].max() for df in strategy_data.values()])

# Add a horizontal line for the maximum value
max_value_line = go.Scatter(
    x=[data['Date'].min(), data['Date'].max()],
    y=[max_value, max_value],
    mode='lines',
    line=dict(color='orange', width=2, dash='dash'),
    name=f'Max Value: ${max_value:,.2f}',
    hoverinfo='skip'
)
fig.add_trace(max_value_line)

# Add annotation for the maximum value line on the left side
fig.add_annotation(
    x=data['Date'].min(),
    y=max_value,
    xref='x',
    yref='y',
    text=f"Max Value: ${max_value:,.2f}",
    showarrow=True,
    arrowhead=2,
    ax=50,  # Adjusted value to position annotation on the left side
    ay=0,
    bgcolor="yellow"
)

# Set the title and labels
fig.update_layout(
    title="Strategy Performance Over Time",
    xaxis_title="Date",
    yaxis_title="Total Money ($)",
    xaxis=dict(showgrid=True),
    yaxis=dict(showgrid=True),
    hovermode="x unified",  # Show hover info for both lines on the same date
    legend=dict(x=0, y=1.1, orientation="h"),
)

# Customize hover label appearance
fig.update_traces(hoverlabel=dict(bgcolor="white", font_size=12, font_family="Rockwell"))

# Show the interactive plot
fig.show()
