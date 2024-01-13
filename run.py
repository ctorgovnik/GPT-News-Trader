# Import necessary modules
from execution import ExecutionBot
from buy_sell import buy_orders, sell_orders
from flask_app import run_flask_app
import news_data
from order_repository import OrderRepository as order_repo
import yfinance as yf
from order_repository_sql import OrderRepositorySQL as order_sql
from category_repository import CategoryRepository as category_repo
from multiprocessing import Process, Manager, Lock, freeze_support
import multiprocessing
import config
import pickle

# Function to check if an object is picklable
def is_picklable(obj):
    try:
        pickle.dumps(obj)
        return True
    except (pickle.PicklingError, TypeError):
        return False

# Function to initialize shared objects
def initialize_shared_objects():
    manager = Manager()
    shared_order_list = manager.list()
    order_lock = Lock()
    bot_lock = Lock()
    trading_mode = manager.Value('c', 'paper')  # Shared value for trading mode
    return order_lock, bot_lock, shared_order_list, trading_mode, Lock()

# Main function
def main():
    order_lock, bot_lock, shared_order_list, trading_mode, lock = initialize_shared_objects()
    
    session = news_data.login()
    bot = ExecutionBot()

    # Create processes
    flask_process = Process(target=run_flask_app, args=(trading_mode, lock))
    buy_process = Process(target=buy_orders, args=(bot, session, shared_order_list, order_lock, bot_lock))
    sell_process = Process(target=sell_orders, args=(bot, shared_order_list, order_lock, bot_lock))

    flask_process.start()
    buy_process.start()
    sell_process.start()

    buy_process.join()
    sell_process.join()

# Entry point of the script
if __name__ == '__main__':
    freeze_support()
    multiprocessing.set_start_method('fork')
    main()

