# src/data_fetching/alpha_vantage.py

from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from src.utils.config import ALPHA_VANTAGE_API_KEY

def fetch_alpha_vantage_data(symbol, api_key=ALPHA_VANTAGE_API_KEY, interval='1min', outputsize='full'):
    """
    Fetch historical data from Alpha Vantage.

    :param symbol: Stock symbol (e.g., 'AAPL')
    :param api_key: API key for Alpha Vantage (default from config)
    :param interval: Interval for data ('1min', '5min', '15min', 'daily')
    :param outputsize: Output size ('full' or 'compact')
    
    :return: DataFrame containing historical data
    """
    ts = TimeSeries(key=api_key, output_format='pandas')

    try:
        # Get intraday data by default
        if interval in ['1min', '5min', '15min']:
            data, _ = ts.get_intraday(symbol=symbol, interval=interval, outputsize=outputsize)
        # Get daily data if 'daily' is selected
        elif interval == 'daily':
            data, _ = ts.get_daily(symbol=symbol, outputsize=outputsize)
        else:
            raise ValueError("Unsupported interval")

        return data
    except Exception as e:
        print(f"Error fetching data from Alpha Vantage: {e}")
        return None
