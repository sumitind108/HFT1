def trading_decision(order_book_data):
    """
    Trading decision logic based on market imbalance.
    """
    if len(order_book_data) == 0:
        print("No order book data available")
        return

    # Check if the 'Type' column exists, if not, add it
    if 'Type' not in order_book_data.columns:
        # Assuming 'order_book_data' consists of both bid and ask, add 'Type' to differentiate
        order_book_data['Type'] = ['Bid'] * len(order_book_data) if order_book_data.iloc[0]['Price'] < order_book_data.iloc[1]['Price'] else ['Ask'] * len(order_book_data)
    
    # Get the latest bid and ask data
    latest_bid = order_book_data[order_book_data['Type'] == 'Bid'].iloc[-1]
    latest_ask = order_book_data[order_book_data['Type'] == 'Ask'].iloc[-1]

    bid_price = float(latest_bid['Price'])
    ask_price = float(latest_ask['Price'])
    bid_quantity = float(latest_bid['Quantity'])
    ask_quantity = float(latest_ask['Quantity'])

    # Calculate imbalance
    total_bid_qty = order_book_data[order_book_data['Type'] == 'Bid']['Quantity'].sum()
    total_ask_qty = order_book_data[order_book_data['Type'] == 'Ask']['Quantity'].sum()
    
    imbalance = total_bid_qty / (total_bid_qty + total_ask_qty)
    
    if imbalance > 0.7:  # Buy condition (Bid side stronger)
        print(f"Imbalance is {imbalance}, consider buying at {ask_price}")
        # Simulate Buy (you can integrate with API for real trades)
    elif imbalance < 0.3:  # Sell condition (Ask side stronger)
        print(f"Imbalance is {imbalance}, consider selling at {bid_price}")
        # Simulate Sell (you can integrate with API for real trades)

