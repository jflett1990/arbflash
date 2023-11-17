import requests

class DataFetchingAgent:
    def __init__(self, binance_api_url, coinbase_api_url):
        self.binance_api_url = binance_api_url
        self.coinbase_api_url = coinbase_api_url

    def fetch_data_from_binance(self):
        # Endpoint for Binance API to fetch market data
        endpoint = '/api/v3/ticker/price'
        try:
            response = requests.get(self.binance_api_url + endpoint)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching data from Binance: {e}")
            return None

    def fetch_data_from_coinbase(self):
        # Endpoint for Coinbase API to fetch market data
        endpoint = '/v2/prices/spot?currency=USD'
        try:
            response = requests.get(self.coinbase_api_url + endpoint)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching data from Coinbase: {e}")
            return None

    def fetch_order_book_binance(self, symbol, limit=100):
        # Binance order book endpoint
        endpoint = f'/api/v3/depth?symbol={symbol}&limit={limit}'
        try:
            response = requests.get(self.binance_api_url + endpoint)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching order book from Binance: {e}")
            return None

    def fetch_order_book_coinbase(self, symbol):
        # Coinbase order book endpoint (level 2 data)
        endpoint = f'/products/{symbol}/book?level=2'
        try:
            response = requests.get(self.coinbase_api_url + endpoint)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching order book from Coinbase: {e}")
            return None

    def fetch_market_data(self):
        # Fetch general market data from both Binance and Coinbase
        binance_data = self.fetch_data_from_binance()
        coinbase_data = self.fetch_data_from_coinbase()
        return {"binance": binance_data, "coinbase": coinbase_data}

# Usage example
binance_api_url = "https://api.binance.com"
coinbase_api_url = "https://api.coinbase.com"
data_agent = DataFetchingAgent(binance_api_url, coinbase_api_url)

# Fetch market data
market_data = data_agent.fetch_market_data()
print("Market Data:", market_data)

# Fetch order book data
binance_order_book = data_agent.fetch_order_book_binance("BTCUSDT")
coinbase_order_book = data_agent.fetch_order_book_coinbase("BTC-USD")
print("Binance Order Book:", binance_order_book)
print("Coinbase Order Book:", coinbase_order_book)
