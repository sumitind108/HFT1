import numpy as np

def pairs_trading_strategy(data1, data2, window=30, threshold=2):
    """
    Implementing Pairs Trading Strategy.
    """
    spread = data1['close'] - data2['close']
    spread_mean = spread.rolling(window=window).mean()
    spread_std = spread.rolling(window=window).std()
    
    z_score = (spread - spread_mean) / spread_std  # Z-Score calculation

    buy_signal = z_score < -threshold  # Buy when Z-score is below the threshold
    sell_signal = z_score > threshold  # Sell when Z-score is above the threshold
    
    if buy_signal.iloc[-1]:
        print(f"Buy {data1['symbol'].iloc[-1]} and Sell {data2['symbol'].iloc[-1]}")
    elif sell_signal.iloc[-1]:
        print(f"Sell {data1['symbol'].iloc[-1]} and Buy {data2['symbol'].iloc[-1]}")
