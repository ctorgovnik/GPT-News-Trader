from execution import ExecutionBot
import alpaca_trade_api as tradeapi

# api = tradeapi.REST()
# api.get_position('AAPL')

bot = ExecutionBot()

# getting position of a stock
print(bot.trading_client.get_open_position('AAPL'))

position = bot.trading_client.get_open_position('AAPL')
unrealized_pl = float(position.unrealized_pl)
print(unrealized_pl)

