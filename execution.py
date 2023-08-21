
from alpaca.trading.client import TradingClient
from alpaca.trading.stream import TradingStream
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce


base_url = 'https://paper-api.alpaca.markets'
alpaca_api_key = 'PK02G82206DGFCCG31D2'
alpaca_secret_key = '2whkuXYnzEMxDkWf4kcMSQuc3B3NuoqiCykLU7Ss'


class ExecutionBot:
    def __init__(self):
        self.trading_client = TradingClient(
            alpaca_api_key, alpaca_secret_key, paper=True)

    def get_account_info(self):
        # Getting account information and printing it
        account = self.trading_client.get_account()
        for property_name, value in account:
            print(f"\"{property_name}\": {value}")

        return account

    def buy_order(self, ticker, qty, time_in_force=TimeInForce.DAY):
        # Setting parameters for our buy order
        market_order_data = MarketOrderRequest(
            symbol=ticker,
            qty=qty,
            side=OrderSide.BUY,
            time_in_force=time_in_force
        )

        # Submitting the order and then printing the returned object
        market_order = self.trading_client.submit_order(market_order_data)
        for property_name, value in market_order:
            print(f"\"{property_name}\": {value}")

        return market_order

    def sell_order(self, ticker, qty, time_in_force=TimeInForce.DAY):
        # Setting parameters for our buy order
        market_order_data = MarketOrderRequest(
            symbol=ticker,
            qty=qty,
            side=OrderSide.SELL,
            time_in_force=time_in_force
        )

        # Submitting the order and then printing the returned object
        market_order = self.trading_client.submit_order(market_order_data)
        for property_name, value in market_order:
            print(f"\"{property_name}\": {value}")
        
        return market_order
        

    def get_positions(self):
        # Get all open positions and print each of them
        positions = self.trading_client.get_all_positions()
        for position in positions:
            for property_name, value in position:
                print(f"\"{property_name}\": {value}")

        return positions

# bot = ExecutionBot()

# # bot.get_account_info()
# bot.get_positions()

# bot.buy_order('AAPL', .01)

# trades = TradingStream(alpaca_api_key, alpaca_secret_key, paper=True)

# async def trade_status(data):
#     print(data)


# trades.subscribe_trade_updates(trade_status)

# trades.run()