# import pandas as pd
# import talib
# import logging

# # Set up logging for the strategy
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
# logger = logging.getLogger(__name__)

# def mean_reversion_strategy(data, window=20, threshold=2):
#     """
#     Implementing Mean Reversion Strategy.
#     """
#     try:
#         # Ensure there is enough data for the rolling window
#         if len(data) < window:
#             logger.warning(f"Not enough data for the window size {window}. Skipping strategy.")
#             return

#         # Calculate the Simple Moving Average (SMA)
#         data['SMA'] = data['close'].rolling(window=window).mean()
#         # Calculate the deviation from the SMA
#         data['deviation'] = data['close'] - data['SMA']

#         # Generate Buy/Sell signals based on deviation from the mean
#         buy_signal = data['deviation'] < -threshold  # Buy when price is below the mean
#         sell_signal = data['deviation'] > threshold  # Sell when price is above the mean

#         # Log Buy/Sell signals
#         if buy_signal.iloc[-1]:
#             logger.info(f"Buy signal at {data['close'].iloc[-1]} on {data.index[-1]}")
#         elif sell_signal.iloc[-1]:
#             logger.info(f"Sell signal at {data['close'].iloc[-1]} on {data.index[-1]}")

#     except Exception as e:
#         logger.error(f"Error occurred in Mean Reversion Strategy: {e}, Data Length: {len(data)}")


# ------------------------------------------


import talib

def mean_reversion_strategy(data):
    if 'close' not in data.columns:
        print("Error: 'close' column missing")
        return
    
    data['RSI'] = talib.RSI(data['close'], timeperiod=14)
    
    # Generate Buy/Sell Signals
    buy_signal = data['RSI'] < 30  # Buy when RSI is below 30 (oversold)
    sell_signal = data['RSI'] > 70  # Sell when RSI is above 70 (overbought)
    
    if buy_signal.iloc[-1]:
        print(f"Buy signal at {data['close'].iloc[-1]}")
    elif sell_signal.iloc[-1]:
        print(f"Sell signal at {data['close'].iloc[-1]}")
