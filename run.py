from execution import ExecutionBot
from buy_sell import buy_orders, sell_orders

import news_data
from order_repository import OrderRepository as order_repo
import yfinance as yf
from order_repository_sql import OrderRepositorySQL as order_sql
from category_repository import CategoryRepository as category_repo
from multiprocessing import Process, Manager, Lock, freeze_support
import multiprocessing
import config

import pickle

def is_picklable(obj):
    try:
        pickle.dumps(obj)
        return True
    except (pickle.PicklingError, TypeError):
        return False

def initialize_shared_objects():
    manager = Manager()
    shared_order_list = manager.list()
    order_lock = Lock()
    bot_lock = Lock()
    
    return order_lock, bot_lock, shared_order_list

def main():
    order_lock, bot_lock, shared_order_list = initialize_shared_objects()
    
    session = news_data.login()
    bot = ExecutionBot()

    # Create processes
    buy_process = Process(target=buy_orders, args=(bot, session, shared_order_list, order_lock, bot_lock))
    sell_process = Process(target=sell_orders, args=(bot, shared_order_list, order_lock, bot_lock))

    buy_process.start()
    sell_process.start()
    buy_process.join()
    sell_process.join()


if __name__ == '__main__':
    freeze_support()
    multiprocessing.set_start_method('spawn')
    main()




