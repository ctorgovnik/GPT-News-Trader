from execution import ExecutionBot
from buy_sell import buy_orders, sell_orders

import news_data
from order_repository import OrderRepository as order_repo
import yfinance as yf
from order_repository_sql import OrderRepositorySQL as order_sql
from category_repository import CategoryRepository as category_repo
from multiprocessing import Process, Manager, Lock
import config

host = config.database_host
username = config.database_username
password = config.database_password
database = config.database

session = news_data.login()
bot = ExecutionBot()
order_repo = order_sql(host=host, user=username, password=password, database=database)
category_repo = category_repo(host=host, user=username, password=password, database=database)

manager = Manager()
shared_order_list = manager.list()
order_lock = Lock()

bot_lock = Lock()

# Create processes
buy_process = Process(target=buy_orders, args=(bot, session, order_repo, category_repo, shared_order_list, order_lock, bot_lock))
sell_process = Process(target=sell_orders, args=(bot, shared_order_list, order_lock, bot_lock, order_repo))


buy_process.start()
sell_process.start()

