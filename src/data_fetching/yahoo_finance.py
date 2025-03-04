import yfinance as yf

def fetch_yahoo_data(ticker, start_date, end_date, interval='1m'):
    """
    Fetch historical data from Yahoo Finance.

    :param ticker: Stock ticker (e.g., 'AAPL')
    :param start_date: Start date for historical data (e.g., '2020-01-01')
    :param end_date: End date for historical data (e.g., '2025-01-01')
    :param interval: Data interval (e.g., '1m', '5m', '1d')

    :return: DataFrame containing historical data
    """
    try:
        data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
        return data
    except Exception as e:
        print(f"Error fetching data from Yahoo Finance: {e}")
        return None
