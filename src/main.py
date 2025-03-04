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

# Import strategy functions
from src.strategies.market_making import trading_decision
from src.strategies.mean_reversion import mean_reversion_strategy
from src.strategies.momentum import momentum_strategy
from src.strategies.pairs_trading import pairs_trading_strategy

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

def apply_strategies(data):
    """
    Apply all trading strategies on the cleaned data.
    """
    try:
        # Log the first few rows of the data to ensure it's correct
        logger.info(f"Data being passed to strategies:\n{data.head()}")
        
        logger.info("Applying Market Making Strategy...")
        trading_decision(data)  # Market Making Strategy

        logger.info("Applying Mean Reversion Strategy...")
        mean_reversion_strategy(data)  # Mean Reversion Strategy

        logger.info("Applying Momentum Strategy...")
        momentum_strategy(data)  # Momentum Strategy

        logger.info("Applying Pairs Trading Strategy...")
        pairs_trading_strategy(data)  # Pairs Trading Strategy
    
    except Exception as e:
        logger.error(f"Error occurred during strategy execution: {e}")

def fetch_and_process_data(symbol, interval):
    """
    Fetch data from Alpha Vantage, clean it, and apply strategies.
    """
    try:
        # Fetch historical data for the given symbol and interval
        logger.info(f"Fetching data for {symbol} ({interval}) from Alpha Vantage.")
        data = fetch_alpha_vantage_data(symbol=symbol, interval=interval, outputsize='full')
        
        if data is not None:
            # Clean the data before passing it to strategies
            cleaned_data = clean_data(data)

            # Save the cleaned data to a CSV file with a timestamp to avoid overwriting
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            save_path = os.path.join('data', 'historical_data', f'{symbol}_{interval}_{timestamp}_data.csv')

            # Check if the file already exists, if so, append or handle versioning
            if os.path.exists(save_path):
                logger.warning(f"File {save_path} already exists. Overwriting the file.")
            else:
                logger.info(f"Saving data to {save_path}")

            cleaned_data.to_csv(save_path, index=False)  # Save without the index
            logger.info(f"Data saved to {save_path}")
            
            # Call strategies with the cleaned data for backtesting
            logger.info(f"Applying strategies for {symbol} ({interval})...")
            apply_strategies(cleaned_data)
            
        else:
            logger.error("No data fetched from Alpha Vantage.")
    
    except Exception as e:
        logger.error(f"Error occurred while fetching or saving data: {e}")

def main(symbol, interval):
    fetch_and_process_data(symbol, interval)

if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Fetch historical stock data from Alpha Vantage.")
    parser.add_argument('--symbol', type=str, required=True, help='Stock symbol (e.g., AAPL, MSFT)')
    parser.add_argument('--interval', type=str, required=True, choices=['1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly'],
                        help="Time interval for fetching the data.")
    args = parser.parse_args()

    # Call the main function with user input
    main(symbol=args.symbol, interval=args.interval)
