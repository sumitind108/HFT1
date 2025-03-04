# import websocket
# import json
# import pandas as pd
# import logging
# import numpy as np
# import time 
# from websocket import create_connection
# from retrying import retry

# # Set up logging for the order book data
# logging.basicConfig(filename="binance_order_book_data.log", level=logging.INFO, format='%(asctime)s - %(message)s')

# # Dataframe to hold the real-time order book data (can be extended)
# order_book_df = pd.DataFrame(columns=['Timestamp', 'Price', 'Quantity', 'Type'])


# @retry(stop_max_attempt_number=5, wait_fixed=2000)  # Retry 5 times with 2-second delay
# def connect_to_websocket():
#     ws = create_connection("wss://stream.binance.com:9443/ws/btcusdt@depth")
#     return ws



# def on_message(ws, message):
#     """
#     Handle incoming WebSocket messages (Order Book Data).

#     :param ws: WebSocket object
#     :param message: Incoming message as JSON string
#     """
#     try:
#         print("Message received")
#         data = json.loads(message)
        
#         # Check if the 'bids' and 'asks' exist in the incoming data
#         bids = data.get('bids', [])
#         asks = data.get('asks', [])

#         if bids and asks:
#             # Process the top bid and ask
#             top_bid = bids[0]  # Highest bid (price, quantity)
#             top_ask = asks[0]  # Lowest ask (price, quantity)

#             print(f"Top Bid: {top_bid}, Top Ask: {top_ask}")

#             # Store this data in the DataFrame
#             order_book_data_bid = {
#                 'Timestamp': pd.to_datetime('now'),
#                 'Price': top_bid[0],  # The price of the highest bid
#                 'Quantity': top_bid[1],  # The quantity of the highest bid
#                 'Type': 'Bid'
#             }

#             # Check if the data is not empty or NA before appending
#             if all(pd.notna([order_book_data_bid['Price'], order_book_data_bid['Quantity']])):
#                 global order_book_df
#                 order_book_df = pd.concat([order_book_df, pd.DataFrame([order_book_data_bid])], ignore_index=True)

#                 # Log the bid data for analysis
#                 logging.info(f"Bid Data: {order_book_data_bid}")

#             # Repeat for Ask data
#             order_book_data_ask = {
#                 'Timestamp': pd.to_datetime('now'),
#                 'Price': top_ask[0],  # The price of the lowest ask
#                 'Quantity': top_ask[1],  # The quantity of the lowest ask
#                 'Type': 'Ask'
#             }

#             # Check if the data is not empty or NA before appending
#             if all(pd.notna([order_book_data_ask['Price'], order_book_data_ask['Quantity']])):
#                 order_book_df = pd.concat([order_book_df, pd.DataFrame([order_book_data_ask])], ignore_index=True)

#                 # Log the ask data for analysis
#                 logging.info(f"Ask Data: {order_book_data_ask}")

#             # Optionally print the last 5 rows of the order book
#             print(order_book_df.tail(5))

#         else:
#             print("No bid or ask data found in the message")

#     except Exception as e:
#         print(f"Error in on_message: {e}")

# def on_open(ws):
#     """
#     Send subscription message when WebSocket connection is opened.

#     :param ws: WebSocket object
#     """
#     print("WebSocket connected. Sending subscription request...")
#     msg = json.dumps({
#         "method": "SUBSCRIBE",
#         "params": ["btcusdt@depth5"],  # Subscribe to the top 5 levels of the BTC/USDT order book
#         "id": 1
#     })
#     ws.send(msg)

# def on_error(ws, error):
#     """
#     Handle error events from WebSocket.

#     :param ws: WebSocket object
#     :param error: Error message
#     """
#     print(f"WebSocket error: {error}")
#     logging.error(f"WebSocket error: {error}")

# def on_close(ws, close_status_code, close_msg):
#     """
#     Handle WebSocket closure events.

#     :param ws: WebSocket object
#     :param close_status_code: WebSocket close status code
#     :param close_msg: WebSocket close message
#     """
#     print(f"WebSocket closed. Status Code: {close_status_code}, Message: {close_msg}")


# def calculate_market_depth(order_book_df):
#     """
#     Calculate the market depth by aggregating bid and ask volumes.
#     :param order_book_df: DataFrame containing bid/ask data
#     :return: Dictionary with total bid and ask volume at different price levels
#     """
#     # Filter bid and ask data
#     bids = order_book_df[order_book_df['Type'] == 'Bid']
#     asks = order_book_df[order_book_df['Type'] == 'Ask']

#     # Group by price and calculate total quantity at each price level
#     bid_depth = bids.groupby('Price')['Quantity'].sum().sort_values(ascending=False)
#     ask_depth = asks.groupby('Price')['Quantity'].sum().sort_values(ascending=True)

#     # Check if there are valid top bid and ask levels
#     if not bid_depth.empty and not ask_depth.empty:
#         top_bid = bid_depth.head(5)  # Top 5 bid levels
#         top_ask = ask_depth.head(5)  # Top 5 ask levels

#         # Calculate bid-ask spread
#         bid_ask_spread = top_ask.index[0] - top_bid.index[0]

#         print(f"Top Bid Depth:\n{top_bid}")
#         print(f"Top Ask Depth:\n{top_ask}")
#         print(f"Bid-Ask Spread: {bid_ask_spread}")

#         return top_bid, top_ask, bid_ask_spread
#     else:
#         print("Insufficient data for calculating market depth.")
#         return None, None, None



# def track_large_orders(order_book_df, threshold=100):
#     """
#     Identify and track large orders in the order book.
#     :param order_book_df: DataFrame containing bid/ask data
#     :param threshold: The minimum quantity for a large order to be flagged
#     :return: None
#     """
#     large_bids = order_book_df[(order_book_df['Type'] == 'Bid') & (order_book_df['Quantity'] > threshold)]
#     large_asks = order_book_df[(order_book_df['Type'] == 'Ask') & (order_book_df['Quantity'] > threshold)]

#     if not large_bids.empty:
#         print(f"Large Bids Detected:\n{large_bids}")

#     if not large_asks.empty:
#         print(f"Large Asks Detected:\n{large_asks}")

#     # You can add further logic to react to these large orders, e.g., triggering alerts or placing trades


# def process_order_book_data(new_data):
#     """
#     Process new incoming data, calculate market depth, and make trading decisions.
#     :param new_data: New order book data
#     :return: None
#     """
#     global order_book_df

#     # Check if the new data contains valid 'Price' and 'Quantity' for Bid/Ask
#     if 'Price' in new_data and 'Quantity' in new_data and new_data['Price'] != '' and new_data['Quantity'] != '':
#         # Ensure that price and quantity are numbers (float), not strings
#         try:
#             new_data['Price'] = float(new_data['Price'])
#             new_data['Quantity'] = float(new_data['Quantity'])
#         except ValueError:
#             print("Invalid price or quantity in new data, skipping this entry.")
#             return

#         # Add the new data to the order book DataFrame
#         order_book_df = pd.concat([order_book_df, pd.DataFrame([new_data])], ignore_index=True)

#         # Calculate the market depth
#         top_bid, top_ask, bid_ask_spread = calculate_market_depth(order_book_df)

#         # Only proceed if we have valid bid and ask data
#         if top_bid is not None and top_ask is not None:
#             # Check if bid_ask_spread is valid (not None) and less than 0.1
#             if bid_ask_spread is not None and bid_ask_spread < 0.1:
#                 print(f"Bid-Ask Spread is narrow: {bid_ask_spread}, considering a trade!")
#                 # Implement your trade logic here

#         else:
#             print("No valid bid or ask data found, unable to calculate market depth.")

#         # Optionally, save to CSV every N entries
#         if len(order_book_df) % 100 == 0:
#             order_book_df.to_csv('binance_order_book_data.csv', index=False)
#     else:
#         print("Invalid data received, skipping this entry.")

#     # Simulate a delay for the next incoming data
#     time.sleep(1)  # Adjust this delay as needed


# # Simulate receiving new order book data
# new_order_data = {
#     'Timestamp': pd.to_datetime('now'),
#     'Price': '85011.98000000',
#     'Quantity': '4.86603000',
#     'Type': 'Bid'
# }

# # Process the data
# process_order_book_data(new_order_data)



# def fetch_binance_order_book():
#     """
#     Establish WebSocket connection and fetch real-time order book data from Binance.
#     """
#     try:
#         print("Connecting to Binance WebSocket...")
#         ws = websocket.WebSocketApp(
#             "wss://stream.binance.com:9443/ws/btcusdt@depth5",
#             on_message=on_message,
#             on_open=on_open,
#             on_error=on_error,
#             on_close=on_close
#         )
#         print("WebSocketApp initialized. Now running forever.")
#         ws.run_forever()  # Keep the WebSocket connection open
#     except Exception as e:
#         print(f"Error in WebSocket connection: {e}")

# # Example usage:
# fetch_binance_order_book()  # Uncomment this line to start fetching data


# ------------------------------------

import websocket
import json
import pandas as pd
import logging
import time 
from websocket import create_connection
from retrying import retry
from src.strategies.market_making import trading_decision
from src.strategies.mean_reversion import mean_reversion_strategy
from src.strategies.momentum import momentum_strategy
from src.strategies.pairs_trading import pairs_trading_strategy


# Set up logging for the order book data
# logging.basicConfig(filename="binance_order_book_data.log", level=logging.INFO, format='%(asctime)s - %(message)s')
logging.basicConfig(filename="data/raw_data/binance_order_book_data.log", level=logging.INFO, format='%(asctime)s - %(message)s')


# Dataframe to hold the real-time order book data (can be extended)
order_book_df = pd.DataFrame(columns=['Timestamp', 'Price', 'Quantity', 'Type'])

@retry(stop_max_attempt_number=5, wait_fixed=2000)  # Retry 5 times with 2-second delay
def connect_to_websocket():
    ws = create_connection("wss://stream.binance.com:9443/ws/btcusdt@depth")
    return ws

def on_message(ws, message):
    """
    Handle incoming WebSocket messages (Order Book Data).
    :param ws: WebSocket object
    :param message: Incoming message as JSON string
    """
    try:
        print("Message received")
        data = json.loads(message)

        # Extract bids and asks from incoming data
        bids = data.get('bids', [])
        asks = data.get('asks', [])

        if bids and asks:
            # Process the top bid and ask
            top_bid = bids[0]  # Highest bid (price, quantity)
            top_ask = asks[0]  # Lowest ask (price, quantity)

            # Prepare bid data
            order_book_data_bid = {
                'Timestamp': pd.to_datetime('now'),
                'Price': top_bid[0],  # The price of the highest bid
                'Quantity': top_bid[1],  # The quantity of the highest bid
                'Type': 'Bid'
            }

            # Append bid data if valid
            if all(pd.notna([order_book_data_bid['Price'], order_book_data_bid['Quantity']])):
                global order_book_df
                if not order_book_data_bid['Price'] or pd.isna(order_book_data_bid['Price']):
                    print("Bid data invalid, skipping")
                else:
                    order_book_df = pd.concat([order_book_df, pd.DataFrame([order_book_data_bid])], ignore_index=True)
                logging.info(f"Bid Data: {order_book_data_bid}")

            # Prepare ask data
            order_book_data_ask = {
                'Timestamp': pd.to_datetime('now'),
                'Price': top_ask[0],  # The price of the lowest ask
                'Quantity': top_ask[1],  # The quantity of the lowest ask
                'Type': 'Ask'
            }

            # Append ask data if valid
            if all(pd.notna([order_book_data_ask['Price'], order_book_data_ask['Quantity']])):
                order_book_df = pd.concat([order_book_df, pd.DataFrame([order_book_data_ask])], ignore_index=True)
                logging.info(f"Ask Data: {order_book_data_ask}")

            print(order_book_df.tail(5))

            # Call trading decision logic after processing new data
            trading_decision(order_book_df)
            mean_reversion_strategy(order_book_df)
            momentum_strategy(order_book_df)
            pairs_trading_strategy(order_book_df)

        else:
            print("No bid or ask data found in the message")

    except Exception as e:
        print(f"Error in on_message: {e}")

def on_open(ws):
    """
    Send subscription message when WebSocket connection is opened.
    :param ws: WebSocket object
    """
    print("WebSocket connected. Sending subscription request...")
    msg = json.dumps({
        "method": "SUBSCRIBE",
        "params": ["btcusdt@depth5"],  # Subscribe to the top 5 levels of the BTC/USDT order book
        "id": 1
    })
    ws.send(msg)

def on_error(ws, error):
    """
    Handle error events from WebSocket.
    :param ws: WebSocket object
    :param error: Error message
    """
    print(f"WebSocket error: {error}")
    logging.error(f"WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    """
    Handle WebSocket closure events.
    :param ws: WebSocket object
    :param close_status_code: WebSocket close status code
    :param close_msg: WebSocket close message
    """
    print(f"WebSocket closed. Status Code: {close_status_code}, Message: {close_msg}")
    time.sleep(5)  # Wait before reconnecting
    fetch_binance_order_book()  # Attempt to reconnect

def calculate_market_depth(order_book_df):
    """
    Calculate the market depth by aggregating bid and ask volumes.
    :param order_book_df: DataFrame containing bid/ask data
    :return: Dictionary with total bid and ask volume at different price levels
    """
    # Filter bid and ask data
    bids = order_book_df[order_book_df['Type'] == 'Bid']
    asks = order_book_df[order_book_df['Type'] == 'Ask']

    # Group by price and calculate total quantity at each price level
    bid_depth = bids.groupby('Price')['Quantity'].sum().sort_values(ascending=False)
    ask_depth = asks.groupby('Price')['Quantity'].sum().sort_values(ascending=True)

    # Check if there are valid top bid and ask levels
    if not bid_depth.empty and not ask_depth.empty:
        top_bid = bid_depth.head(5)  # Top 5 bid levels
        top_ask = ask_depth.head(5)  # Top 5 ask levels

        # Calculate bid-ask spread
        bid_ask_spread = top_ask.index[0] - top_bid.index[0]

        print(f"Top Bid Depth:\n{top_bid}")
        print(f"Top Ask Depth:\n{top_ask}")
        print(f"Bid-Ask Spread: {bid_ask_spread}")

        return top_bid, top_ask, bid_ask_spread
    else:
        print("Insufficient data for calculating market depth.")
        return None, None, None

def track_large_orders(order_book_df, threshold=100):
    """
    Identify and track large orders in the order book.
    :param order_book_df: DataFrame containing bid/ask data
    :param threshold: The minimum quantity for a large order to be flagged
    :return: None
    """
    large_bids = order_book_df[(order_book_df['Type'] == 'Bid') & (order_book_df['Quantity'] > threshold)]
    large_asks = order_book_df[(order_book_df['Type'] == 'Ask') & (order_book_df['Quantity'] > threshold)]

    if not large_bids.empty:
        print(f"Large Bids Detected:\n{large_bids}")

    if not large_asks.empty:
        print(f"Large Asks Detected:\n{large_asks}")

    # You can add further logic to react to these large orders, e.g., triggering alerts or placing trades



def process_order_book_data(new_data):
    """
    Process new incoming data, calculate market depth, and make trading decisions.
    :param new_data: New order book data
    :return: None
    """
    global order_book_df

    # Check if the new data contains valid 'Price' and 'Quantity' for Bid/Ask
    if 'Price' in new_data and 'Quantity' in new_data and new_data['Price'] != '' and new_data['Quantity'] != '':
        # Ensure that price and quantity are numbers (float), not strings
        try:
            new_data['Price'] = float(new_data['Price'])
            new_data['Quantity'] = float(new_data['Quantity'])
        except ValueError:
            print("Invalid price or quantity in new data, skipping this entry.")
            return

        # Add the new data to the order book DataFrame
        order_book_df = pd.concat([order_book_df, pd.DataFrame([new_data])], ignore_index=True)

        # Calculate the market depth
        top_bid, top_ask, bid_ask_spread = calculate_market_depth(order_book_df)

        # Only proceed if we have valid bid and ask data
        if top_bid is not None and top_ask is not None:
            # Check if bid_ask_spread is valid (not None) and less than 0.1
            if bid_ask_spread is not None and bid_ask_spread < 0.1:
                print(f"Bid-Ask Spread is narrow: {bid_ask_spread}, considering a trade!")
                # Implement your trade logic here

        else:
            print("No valid bid or ask data found, unable to calculate market depth.")

        # Optionally, save to CSV every N entries
        if len(order_book_df) % 100 == 0:
            order_book_df.to_csv('binance_order_book_data.csv', index=False)
    else:
        print("Invalid data received, skipping this entry.")

    # Simulate a delay for the next incoming data
    time.sleep(1)  # Adjust this delay as needed

def fetch_binance_order_book():
    """
    Establish WebSocket connection and fetch real-time order book data from Binance.
    """
    try:
        print("Connecting to Binance WebSocket...")
        ws = websocket.WebSocketApp(
            "wss://stream.binance.com:9443/ws/btcusdt@depth5",
            on_message=on_message,
            on_open=on_open,
            on_error=on_error,
            on_close=on_close
        )
        print("WebSocketApp initialized. Now running forever.")
        ws.run_forever()  # Keep the WebSocket connection open
    except Exception as e:
        print(f"Error in WebSocket connection: {e}")
        time.sleep(5)  # Reattempt connection after a delay

# Example usage:
fetch_binance_order_book()  # Uncomment this line to start fetching data
