import pandas as pd

def generate_order_book_data():
    """
    Generate some simulated order book data for the market-making strategy.
    For now, this function will generate random order book data.
    """
    # Simulated data (usually, this would come from an exchange or a real-time data source)
    data = {
        'Price': [100.1, 100.2, 100.3, 100.4, 100.5, 100.6, 100.7, 100.8],
        'Quantity': [5, 10, 5, 8, 12, 7, 9, 6],
    }

    # Create DataFrame to represent order book
    order_book_data = pd.DataFrame(data)

    # Add a 'Type' column based on simple price logic
    # For example, prices lower than the next one are 'Bid', higher are 'Ask'
    order_book_data['Type'] = ['Bid' if order_book_data['Price'][i] < order_book_data['Price'][i+1] else 'Ask' 
                               for i in range(len(order_book_data)-1)] + ['Ask']  # Last one is assumed to be 'Ask'

    return order_book_data


def trading_decision(order_book_data):
    """
    Trading decision logic based on market imbalance.
    """
    if order_book_data.empty:
        print("No order book data available")
        return

    required_columns = ['Price', 'Quantity']
    missing_cols = [col for col in required_columns if col not in order_book_data.columns]
    if missing_cols:
        print(f"Missing required columns: {', '.join(missing_cols)}")
        return

    # Set 'Type' column if it doesn't exist
    if 'Type' not in order_book_data.columns:
        order_book_data['Type'] = ['Bid' if order_book_data.iloc[i]['Price'] < order_book_data.iloc[i+1]['Price'] else 'Ask' for i in range(len(order_book_data)-1)]

    # Calculate imbalance and decision logic
    total_bid_qty = order_book_data[order_book_data['Type'] == 'Bid']['Quantity'].sum()
    total_ask_qty = order_book_data[order_book_data['Type'] == 'Ask']['Quantity'].sum()

    imbalance = total_bid_qty / (total_bid_qty + total_ask_qty)
    latest_bid = order_book_data[order_book_data['Type'] == 'Bid'].iloc[-1]
    latest_ask = order_book_data[order_book_data['Type'] == 'Ask'].iloc[-1]

    # Trading Decision
    if imbalance > 0.7:  # Buy condition
        print(f"Imbalance is {imbalance}, consider buying at {latest_ask['Price']}")
    elif imbalance < 0.3:  # Sell condition
        print(f"Imbalance is {imbalance}, consider selling at {latest_bid['Price']}")
