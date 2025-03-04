import talib

def momentum_strategy(data):
    """
    Implementing Momentum Strategy using RSI.
    """
    data['RSI'] = talib.RSI(data['close'], timeperiod=14)
    
    buy_signal = data['RSI'] < 30  # Buy when RSI is below 30 (oversold)
    sell_signal = data['RSI'] > 70  # Sell when RSI is above 70 (overbought)
    
    if buy_signal.iloc[-1]:
        print(f"Buy signal at {data['close'].iloc[-1]}")
    elif sell_signal.iloc[-1]:
        print(f"Sell signal at {data['close'].iloc[-1]}")
