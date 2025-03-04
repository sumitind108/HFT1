from kiteconnect import KiteTicker
import pandas as pd
import logging
from datetime import datetime

# Set up logging for the order book data
logging.basicConfig(filename="zerodha_order_book_data.log", level=logging.INFO, format='%(asctime)s - %(message)s')

# Dataframe to hold the real-time data (can be extended)
order_book_df = pd.DataFrame(columns=['Timestamp', 'Price', 'Quantity', 'Type'])

def on_ticks(ws, ticks):
    """
    Handle incoming ticks (order book data) from Zerodha.

    :param ws: WebSocket object
    :param ticks: List of ticks (real-time order book data)
    """
    try:
        # Extract bid and ask data
        for tick in ticks:
            # Extract the data we need (usually, price and quantity)
            price = tick.get('last_price')  # Last traded price
            quantity = tick.get('quantity')  # Quantity of the trade

            if price and quantity:
                # Construct the data to store in the DataFrame
                order_book_data = {
                    'Timestamp': datetime.now(),
                    'Price': price,
                    'Quantity': quantity,
                    'Type': 'Bid' if tick['tradable'] == 'buy' else 'Ask'  # Adjust as per the available tick data type
                }

                # Add the new data to the order book DataFrame
                global order_book_df
                order_book_df = order_book_df.append(order_book_data, ignore_index=True)

                # Log the order book data for analysis
                logging.info(f"Order Book Data: {order_book_data}")

                # Optionally print the latest data
                print(order_book_df.tail(5))  # Print the last 5 rows for quick inspection

    except Exception as e:
        print(f"Error in on_ticks: {e}")

def on_connect(ws, response):
    """
    Handle the connection event for Zerodha WebSocket.
    :param ws: WebSocket object
    :param response: Response data from the WebSocket connection
    """
    print("WebSocket connected successfully.")

def on_close(ws, code, reason):
    """
    Handle the close event for Zerodha WebSocket.
    :param ws: WebSocket object
    :param code: Closing code
    :param reason: Reason for closing
    """
    print("WebSocket closed. Code:", code, "Reason:", reason)

def fetch_zerodha_order_book(api_key, access_token, instrument_token):
    """
    Fetch real-time order book data from Zerodha using KiteTicker.

    :param api_key: API key for Zerodha
    :param access_token: Access token for Zerodha
    :param instrument_token: Token for the instrument (e.g., Reliance stock)
    """
    kws = KiteTicker(api_key, access_token)

    # Assign event handlers
    kws.on_ticks = on_ticks
    kws.on_connect = on_connect
    kws.on_close = on_close

    # Subscribe to the instrument's order book (e.g., Reliance)
    kws.subscribe([instrument_token])  # Pass the instrument token to subscribe to its data

    # Start the WebSocket connection
    kws.connect(threaded=True)

# Example usage:
# fetch_zerodha_order_book("your_api_key", "your_access_token", 738561)  # Replace with your API details
