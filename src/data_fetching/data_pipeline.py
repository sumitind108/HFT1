from yahoo_finance import fetch_yahoo_data
from alpha_vantage import fetch_alpha_vantage_data
from binance_websocket import fetch_binance_order_book
from zerodha_websocket import fetch_zerodha_order_book

def fetch_historical_data(source, symbol, start_date, end_date, interval='1m', api_key=None):
    """
    Fetch historical data based on the source.

    :param source: Data source ('yahoo', 'alpha_vantage')
    :param symbol: Stock symbol (e.g., 'AAPL')
    :param start_date: Start date for historical data
    :param end_date: End date for historical data
    :param interval: Interval for data
    :param api_key: API key (if needed for source)
    """
    if source == 'yahoo':
        return fetch_yahoo_data(symbol, start_date, end_date, interval)
    elif source == 'alpha_vantage':
        return fetch_alpha_vantage_data(symbol, api_key, interval)
    else:
        print("Unknown data source")
        return None

def fetch_real_time_order_book(source, api_key=None, access_token=None, instrument_token=None):
    """
    Fetch real-time order book data based on the source.

    :param source: Data source ('binance', 'zerodha')
    :param api_key: API key for the source (if needed)
    :param access_token: Access token for Zerodha (if needed)
    :param instrument_token: Instrument token for Zerodha (if needed)
    """
    if source == 'binance':
        fetch_binance_order_book()
    elif source == 'zerodha':
        fetch_zerodha_order_book(api_key, access_token, instrument_token)
    else:
        print("Unknown source for real-time data")
