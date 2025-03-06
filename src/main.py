# # src/main.py

# import os
# import logging
# import argparse
# from src.data_fetching.alpha_vantage import fetch_alpha_vantage_data
# import pandas as pd
# from datetime import datetime

# # Set up logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
# logger = logging.getLogger(__name__)

# def main(symbol, interval):
#     try:
#         # Fetch historical data for the given symbol and interval
#         logger.info(f"Fetching data for {symbol} ({interval}) from Alpha Vantage.")
#         data = fetch_alpha_vantage_data(symbol=symbol, interval=interval, outputsize='full')
        
#         if data is not None:
#             # Display the top 5 rows of fetched data
#             logger.info(f"Fetched Data for {symbol} ({interval}):")
#             logger.info(f"\n{data.head()}")  # Show the first 5 rows

#             # Save the fetched data to a CSV file with a timestamp to avoid overwriting
#             timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#             save_path = os.path.join('data', 'historical_data', f'{symbol}_{interval}_{timestamp}_data.csv')

#             # Check if the file already exists, if so, append or handle versioning
#             if os.path.exists(save_path):
#                 logger.warning(f"File {save_path} already exists. Overwriting the file.")
#             else:
#                 logger.info(f"Saving data to {save_path}")

#             data.to_csv(save_path, index=False)  # Save without the index
#             logger.info(f"Data saved to {save_path}")
#         else:
#             logger.error("No data fetched from Alpha Vantage.")
    
#     except Exception as e:
#         logger.error(f"Error occurred while fetching or saving data: {e}")

# if __name__ == "__main__":
#     # Set up command-line argument parsing
#     parser = argparse.ArgumentParser(description="Fetch historical stock data from Alpha Vantage.")
#     parser.add_argument('--symbol', type=str, required=True, help='Stock symbol (e.g., AAPL, MSFT)')
#     parser.add_argument('--interval', type=str, required=True, choices=['1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly'],
#                         help="Time interval for fetching the data.")
#     args = parser.parse_args()

#     # Call the main function with user input
#     main(symbol=args.symbol, interval=args.interval)

# --------------------------------------------------------------------------
# ----------------------------------------------------------------------------


# # src/main.py

# import os
# import logging
# import argparse
# from src.data_fetching.alpha_vantage import fetch_alpha_vantage_data
# import pandas as pd
# from datetime import datetime

# # Import strategy functions
# from src.strategies.market_making import trading_decision
# from src.strategies.mean_reversion import mean_reversion_strategy
# from src.strategies.momentum import momentum_strategy
# from src.strategies.pairs_trading import pairs_trading_strategy

# # Set up logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
# logger = logging.getLogger(__name__)

# def main(symbol, interval):
#     try:
#         # Fetch historical data for the given symbol and interval
#         logger.info(f"Fetching data for {symbol} ({interval}) from Alpha Vantage.")
#         data = fetch_alpha_vantage_data(symbol=symbol, interval=interval, outputsize='full')
        
#         if data is not None:
#             # Display the top 5 rows of fetched data
#             logger.info(f"Fetched Data for {symbol} ({interval}):")
#             logger.info(f"\n{data.head()}")  # Show the first 5 rows

#             # Save the fetched data to a CSV file with a timestamp to avoid overwriting
#             timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#             save_path = os.path.join('data', 'historical_data', f'{symbol}_{interval}_{timestamp}_data.csv')

#             # Check if the file already exists, if so, append or handle versioning
#             if os.path.exists(save_path):
#                 logger.warning(f"File {save_path} already exists. Overwriting the file.")
#             else:
#                 logger.info(f"Saving data to {save_path}")

#             data.to_csv(save_path, index=False)  # Save without the index
#             logger.info(f"Data saved to {save_path}")
            
#             # Call strategies with the fetched data for backtesting
#             logger.info(f"Applying strategies for {symbol} ({interval})...")
#             # Example: Call each strategy (this may vary based on how strategies are structured)
#             trading_decision(data)           # For Market Making
#             mean_reversion_strategy(data)    # For Mean Reversion
#             momentum_strategy(data)          # For Momentum
#             pairs_trading_strategy(data)     # For Pairs Trading
            
#         else:
#             logger.error("No data fetched from Alpha Vantage.")
    
#     except Exception as e:
#         logger.error(f"Error occurred while fetching or saving data: {e}")

# if __name__ == "__main__":
#     # Set up command-line argument parsing
#     parser = argparse.ArgumentParser(description="Fetch historical stock data from Alpha Vantage.")
#     parser.add_argument('--symbol', type=str, required=True, help='Stock symbol (e.g., AAPL, MSFT)')
#     parser.add_argument('--interval', type=str, required=True, choices=['1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly'],
#                         help="Time interval for fetching the data.")
#     args = parser.parse_args()

#     # Call the main function with user input
#     main(symbol=args.symbol, interval=args.interval)

# -------------------------------------------------------
# ---------------------------------------------------------

# src/main.py

import os
import logging
import argparse
from src.data_fetching.alpha_vantage import fetch_alpha_vantage_data
import pandas as pd
from datetime import datetime
import time

# Import strategy functions
from src.strategies.market_making import trading_decision
from src.strategies.mean_reversion import mean_reversion_strategy
from src.strategies.momentum import momentum_strategy
from src.strategies.pairs_trading import pairs_trading_strategy
from src.strategies.market_making import generate_order_book_data 

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def clean_data(data):
    """
    Clean the fetched data to ensure consistency before applying strategies.
    - Handling missing values, etc.
    """
    # Drop rows with NaN values (if any)
    cleaned_data = data.dropna()
    
    # Optionally, you can handle other edge cases like negative prices or invalid data types here
    logger.info(f"Cleaned data. Number of rows after cleaning: {len(cleaned_data)}")
    
    return cleaned_data


def apply_strategies(symbol1, symbol2, data_symbol1, data_symbol2):
    """
    Apply all trading strategies on the cleaned data.
    """
    try:
        logger.info(f"Applying strategies for {symbol1} and {symbol2}")

        # Apply Market Making Strategy
        try:
            logger.info("Applying Market Making Strategy...")
            order_book_data = generate_order_book_data()  # This function must be defined if using market-making
            trading_decision(order_book_data)
        except Exception as e:
            logger.error(f"Error applying Market Making Strategy: {e}")

        # Apply Mean Reversion Strategy
        try:
            logger.info("Applying Mean Reversion Strategy...")
            mean_reversion_strategy(data_symbol1)
        except Exception as e:
            logger.error(f"Error applying Mean Reversion Strategy: {e}")

        # Apply Momentum Strategy
        try:
            logger.info("Applying Momentum Strategy...")
            momentum_strategy(data_symbol1)
        except Exception as e:
            logger.error(f"Error applying Momentum Strategy: {e}")

        # Apply Pairs Trading Strategy
        try:
            logger.info("Applying Pairs Trading Strategy...")
            pairs_trading_strategy(data_symbol1, data_symbol2, window=30, threshold=2)
        except Exception as e:
            logger.error(f"Error applying Pairs Trading Strategy: {e}")

    except Exception as e:
        logger.error(f"Error occurred during strategy execution: {e}")



def fetch_and_process_data(symbol1, symbol2, interval, retries=3, delay=5):
    """
    Fetch data for two symbols, clean it, and apply strategies for pairs trading.
    """
    attempt = 0
    while attempt < retries:
        try:
            logger.info(f"Fetching data for {symbol1} and {symbol2} ({interval}) from Alpha Vantage. Attempt {attempt + 1}...")
            
            # Fetch data for both symbols
            data_symbol1 = fetch_alpha_vantage_data(symbol=symbol1, interval=interval, outputsize='full')
            data_symbol2 = fetch_alpha_vantage_data(symbol=symbol2, interval=interval, outputsize='full')
            
            # Check if data for both symbols is fetched
            if data_symbol1 is not None and not data_symbol1.empty and data_symbol2 is not None and not data_symbol2.empty:
                
                # Log the first few rows of the fetched data to inspect the structure
                logger.info(f"Data for {symbol1}:\n{data_symbol1.head()}")
                logger.info(f"Data for {symbol2}:\n{data_symbol2.head()}")
                
                # Reset index so 'date' becomes a column
                data_symbol1.reset_index(inplace=True)
                data_symbol2.reset_index(inplace=True)
                
                # Rename the columns to match expected names
                data_symbol1.rename(columns={
                    '1. open': 'open',
                    '2. high': 'high',
                    '3. low': 'low',
                    '4. close': 'close',
                    '5. volume': 'volume'
                }, inplace=True)
                
                data_symbol2.rename(columns={
                    '1. open': 'open',
                    '2. high': 'high',
                    '3. low': 'low',
                    '4. close': 'close',
                    '5. volume': 'volume'
                }, inplace=True)
                
                # Log the column names after renaming
                logger.info(f"Columns after renaming for {symbol1}: {data_symbol1.columns}")
                logger.info(f"Columns after renaming for {symbol2}: {data_symbol2.columns}")
                
                # Ensure 'date' and 'close' are present as columns
                if 'date' in data_symbol1.columns and 'close' in data_symbol1.columns and 'date' in data_symbol2.columns and 'close' in data_symbol2.columns:
                    
                    # Clean data for both symbols
                    cleaned_data_symbol1 = clean_data(data_symbol1)
                    cleaned_data_symbol2 = clean_data(data_symbol2)
                    
                    # Combine the data for both symbols (e.g., merge based on dates)
                    combined_data = pd.merge(cleaned_data_symbol1[['date', 'close']], 
                                             cleaned_data_symbol2[['date', 'close']], 
                                             on='date', 
                                             suffixes=(f'_{symbol1}', f'_{symbol2}'))
                    
                    # Save the combined cleaned data to a CSV file with a timestamp
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    
                    # Sanitize the symbol and interval for valid filenames
                    symbol1_safe = symbol1.replace('/', '_').replace(':', '_')
                    symbol2_safe = symbol2.replace('/', '_').replace(':', '_')
                    interval_safe = interval.replace('/', '_')

                    save_path = os.path.join('data', 'historical_data', f'{symbol1_safe}_{symbol2_safe}_{interval_safe}_{timestamp}_data.csv')

                    # Ensure the directory exists
                    os.makedirs(os.path.dirname(save_path), exist_ok=True)

                    # Check if the file already exists
                    if os.path.exists(save_path):
                        logger.warning(f"File {save_path} already exists. Overwriting the file.")
                    else:
                        logger.info(f"Saving data to {save_path}")

                    # Save the combined data to a CSV file
                    combined_data.to_csv(save_path, index=False)
                    logger.info(f"Data saved to {save_path}")
                    
                    # Apply strategies to the combined data
                    logger.info(f"Applying pairs trading strategy for {symbol1} and {symbol2} ({interval})...")
                    apply_strategies(symbol1, symbol2, cleaned_data_symbol1, cleaned_data_symbol2)
                    return  # Data fetched and processed successfully, exit the loop

                else:
                    logger.error(f"Missing expected columns ('date', 'close') in the data for {symbol1} and {symbol2}.")
                    return  # Exit on failure

            else:
                logger.error(f"No valid data fetched for {symbol1} and {symbol2} ({interval}).")
                return  # Exit on failure

        except Exception as e:
            logger.error(f"Error occurred during fetch attempt {attempt + 1}: {e}")
            attempt += 1
            if attempt < retries:
                logger.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logger.error(f"Failed to fetch data after {retries} attempts.")
                return  # Exit after max retries



def main(symbol1, symbol2, interval):
    fetch_and_process_data(symbol1, symbol2, interval)

if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Fetch historical stock data from Alpha Vantage.")
    parser.add_argument('--symbol1', type=str, required=True, help='First stock symbol (e.g., AAPL, MSFT)')
    parser.add_argument('--symbol2', type=str, required=True, help='Second stock symbol (e.g., TSLA, MSFT)')
    parser.add_argument('--interval', type=str, required=True, choices=['1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly'],
                        help="Time interval for fetching the data.")
    args = parser.parse_args()

    # Call the main function with user input
    main(symbol1=args.symbol1, symbol2=args.symbol2, interval=args.interval)



