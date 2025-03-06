import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import logging

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def pairs_trading_strategy(data1, data2, window=30, threshold=2, symbol1="AAPL", symbol2="MSFT"):
    # Validate columns
    if not all(col in data1.columns for col in ['date', 'close']) or not all(col in data2.columns for col in ['date', 'close']):
        logger.error("Error: 'date' or 'close' column missing in the data.")
        return
    
    # Merge data on 'date'
    merged_data = pd.merge(data1[['date', 'close']], data2[['date', 'close']], on='date', suffixes=(f'_{symbol1}', f'_{symbol2}'))

    # Calculate spread, mean, and std
    merged_data['spread'] = merged_data[f'close_{symbol1}'] - merged_data[f'close_{symbol2}']
    merged_data['spread_mean'] = merged_data['spread'].rolling(window=window).mean()
    merged_data['spread_std'] = merged_data['spread'].rolling(window=window).std()
    merged_data['z_score'] = (merged_data['spread'] - merged_data['spread_mean']) / merged_data['spread_std']

    # Buy/Sell Signal based on Z-Score
    merged_data['buy_signal'] = merged_data['z_score'] < -threshold
    merged_data['sell_signal'] = merged_data['z_score'] > threshold

    # Log signals
    logger.info(f"Last few rows of merged data:\n{merged_data[['date', 'z_score', 'buy_signal', 'sell_signal']].tail()}")
    
    # Make Trading Decisions
    if merged_data['buy_signal'].iloc[-1]:
        logger.info(f"Buy {symbol1} and Sell {symbol2}")
    elif merged_data['sell_signal'].iloc[-1]:
        logger.info(f"Sell {symbol1} and Buy {symbol2}")

    # Optional: Plotting the spread and Z-score for visualization
    plot_pairs_trading_results(merged_data, symbol1, symbol2)


    return merged_data[['date', 'spread', 'spread_mean', 'spread_std', 'z_score', 'buy_signal', 'sell_signal']]


def plot_pairs_trading_results(merged_data, symbol1, symbol2):
    """
    Visualize the spread and Z-score over time.

    :param merged_data: The merged DataFrame containing the spread and Z-score
    :param symbol1: Symbol for the first stock (e.g., AAPL)
    :param symbol2: Symbol for the second stock (e.g., MSFT)
    """
    # Plot Spread and Z-Score
    plt.figure(figsize=(12, 6))

    # Plot Spread and Moving Average
    plt.subplot(2, 1, 1)
    plt.plot(merged_data['date'], merged_data['spread'], label='Spread', color='blue')
    plt.plot(merged_data['date'], merged_data['spread_mean'], label='Rolling Mean', color='orange')
    plt.title(f"Spread and Rolling Mean for {symbol1} and {symbol2}")
    plt.legend()

    # Plot Z-Score
    plt.subplot(2, 1, 2)
    plt.plot(merged_data['date'], merged_data['z_score'], label='Z-Score', color='green')
    plt.axhline(y=-2, color='red', linestyle='--', label='Buy Threshold')
    plt.axhline(y=2, color='red', linestyle='--', label='Sell Threshold')
    plt.title(f"Z-Score for {symbol1} and {symbol2}")
    plt.legend()

    # Show the plots
    plt.tight_layout()
    plt.show()

