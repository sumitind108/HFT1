import talib

def momentum_strategy(data):
    if 'close' not in data.columns:
        print("Error: 'close' column missing")
        return
    
    data['RSI'] = talib.RSI(data['close'], timeperiod=14)
    
    # Conditions for Buy and Sell Signals
    buy_signal = data['RSI'] < 30
    sell_signal = data['RSI'] > 70
    
    if buy_signal.iloc[-1]:
        print(f"Buy signal at {data['close'].iloc[-1]}")
    elif sell_signal.iloc[-1]:
        print(f"Sell signal at {data['close'].iloc[-1]}")
