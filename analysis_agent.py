import json

class AnalysisAgent:
    def __init__(self, default_transaction_cost_percentage=0.1, data_format_config=None):
        self.transaction_cost_percentage = default_transaction_cost_percentage
        self.data_format_config = data_format_config or {}

    def update_transaction_cost(self, new_cost_percentage):
        """
        Update the transaction cost percentage.
        """
        self.transaction_cost_percentage = new_cost_percentage

    def update_data_format_config(self, new_format_config):
        """
        Update the data format configuration.
        """
        self.data_format_config = new_format_config

    def parse_market_data(self, market_data):
        """
        Parse the market data based on the provided format configuration.
        """
        try:
            # Assuming the data_format_config contains mappings like:
            # {"BTCUSD": "path.to.BTCUSD.in.market_data", ...}
            parsed_data = {k: eval(f"market_data{self.data_format_config[k]}") for k in self.data_format_config}
            return parsed_data
        except Exception as e:
            print(f"Error parsing market data: {e}")
            return {}

    def calculate_arbitrage_opportunity(self, price_A_B, price_B_C, price_C_A):
        # Starting with 1 unit of Currency A
        initial_amount_A = 1

        # Applying transaction cost for the first trade
        initial_amount_A_after_cost = initial_amount_A * (1 - self.transaction_cost_percentage / 100)

        # Step 1: Convert Currency A to Currency B
        amount_B = initial_amount_A_after_cost / price_A_B

        # Apply transaction cost for the second trade
        amount_B_after_cost = amount_B * (1 - self.transaction_cost_percentage / 100)

        # Step 2: Convert Currency B to Currency C
        amount_C = amount_B_after_cost / price_B_C

        # Apply transaction cost for the third trade
        amount_C_after_cost = amount_C * (1 - self.transaction_cost_percentage / 100)

        # Step 3: Convert Currency C back to Currency A
        final_amount_A = amount_C_after_cost / price_C_A

        # Calculate profit
        profit = final_amount_A - initial_amount_A
        profit_percentage = (profit / initial_amount_A) * 100

        # Determine if this is a profitable opportunity
        if profit_percentage > self.threshold_profit_percentage:
            return {
                'opportunity': True,
                'profit': profit,
                'profit_percentage': profit_percentage
            }
        else:
            return {'opportunity': False}

        pass
    
    def analyze_data(self, market_data):
        """
        Analyze the market data for arbitrage opportunities.
        """
        parsed_data = self.parse_market_data(market_data)
        if parsed_data:
            # Extracting necessary prices from parsed_data
            try:
                price_A_B = parsed_data['BTCUSD']
                price_B_C = parsed_data['ETHBTC']
                price_C_A = 1 / parsed_data['ETHUSD']

                return self.calculate_arbitrage_opportunity(price_A_B, price_B_C, price_C_A)
            except KeyError as e:
                print(f"Missing data in parsed_data: {e}")
                return {'opportunity': False}
        else:
            return {'opportunity': False}

# Example Usage
analysis_agent = AnalysisAgent()
analysis_agent.update_transaction_cost(0.05)  # Update transaction cost to 0.05%

# Define a data format configuration
data_format_config = {
    'BTCUSD': "['BTCUSD']",
    'ETHBTC': "['ETHBTC']",
    'ETHUSD': "['ETHUSD']"
}
analysis_agent.update_data_format_config(data_format_config)

# Sample market data (the structure should match the updated format)
market_data = {
    'BTCUSD': 50000,
    'ETHBTC': 0.06,
    'ETHUSD': 3000
}
opportunity = analysis_agent.analyze_data(market_data)
print(opportunity)
