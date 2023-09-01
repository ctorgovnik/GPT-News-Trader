import news_data
import prompttrainer as pt
from prompttrainer import NewsGpt
import time
import config
from order import Order
import yfinance as yf
import yfinance as yf
from datetime import datetime
from order_repository_sql import OrderRepositorySQL as order_sql
from category_repository import CategoryRepository as category_repo
from alpaca_orders_repo import AlpacaOrderRepository as alpaca_sql
import pytz

def get_latest_price(ticker):
    # fetches 1-minute interval data for the last 2 minutes (to ensure you get at least one data point)
    data = yf.download(ticker, interval="1m", period="2m")
    # get the last available closing price
    return data['Close'].iloc[-1] 

def is_before_market_close():
    # Get the current time in UTC
    current_time_utc = datetime.now(pytz.utc)
    
    # Convert to Eastern Time
    eastern_time = current_time_utc.astimezone(pytz.timezone('US/Eastern'))
    
    return eastern_time.hour < 16 and (eastern_time.hour <= 15 and eastern_time.minute <= 40)


def buy_orders(bot, session, shared_order_list, order_lock, bot_lock):
   
    host = config.database_host
    username = config.database_username
    password = config.database_password
    database = config.database

    order_repo = order_sql(host=host, user=username, password=password, database=database)
    category_repo1 = category_repo(host=host, user=username, password=password, database=database)
    alpaca_repo = alpaca_sql(host=host, user=username, password=password, database=database)
    previous_link = ""
    id = 0
    while True:
        id +=1
        print("start buy process")
        print(shared_order_list)
        article_link = news_data.get_latest_article_link(session)
        if article_link is not None:
            print(article_link)
            if (article_link != previous_link):
                previous_link = article_link

                article_headline, article_time, _, article_text, _ = news_data.get_article_content(
                    article_link, session)

                news_gpt = NewsGpt()
                news_gpt.categorize_article(article_text)

                tickers_list = news_gpt.ticker.split(',')
                for ticker in tickers_list:
                    ticker = ticker.strip()

                    if news_gpt.classification == "Breaking and Positive":
                        news_gpt.classify_breaking_positive(
                            article_text, news_gpt.ticker)
                        if news_gpt.ticker != "N/A" and is_before_market_close():
                            with bot_lock:
                                bot.buy_order(news_gpt.ticker, 1)
                                latest_price = get_latest_price(news_gpt.ticker)
                                current_time = datetime.now()
                                print(f"buying 1 of {news_gpt.ticker} at {latest_price} ({current_time})")
                            # After executing the order, create a new order instance
                            # Assuming you've set up the Order class correctly.
                            new_order = Order(
                                id, news_gpt.ticker, 'paper', 1, get_latest_price(news_gpt.ticker), news_gpt.classification_breaking_positive)

                            # use the lock to safely add this order to the shared list
                            with order_lock:
                                shared_order_list.append(new_order)
                                alpaca_repo.add_order(news_gpt.ticker, 'paper', news_gpt.classification_breaking_positive, 1)

                            order_repo.add_order(
                                article_headline, news_gpt.ticker, news_gpt.classification_breaking_positive, 1)

                category_repo1.add_classification(article_headline, news_gpt.ticker, news_gpt.classification,
                                                    news_gpt.classification_breaking_positive, article_time, article_link)

                print(news_gpt)
                gpt_response = str(news_gpt)
                recipients = config.vonage_recipients
                message = pt.send_text_message(gpt_response, recipients)
            else:
                print("no new articles")
        else:
            print('article is none')

        time.sleep(60)


def sell_orders(bot, shared_order_list, order_lock, bot_lock):
    host = config.database_host
    username = config.database_username
    password = config.database_password
    database = config.database
    order_repo = order_sql(host=host, user=username, password=password, database=database)
    alpaca_repo = alpaca_sql(host=host, user=username, password=password, database=database)

    while True:
        print("start sell process")
        with order_lock:
            for order in shared_order_list:
                if (order.open):
                    with bot_lock:
                        position = bot.trading_client.get_open_position(
                            order.ticker)
                        unrealized_plpc = float(position.unrealized_plpc)
                        if (unrealized_plpc >= .01):
                            bot.sell_order(order.ticker, order.quantity)
                            current_time = datetime.now()
                            order.close_order(current_time, float(position.unrealized_pl), unrealized_plpc)
                            
                            alpaca_repo.modify_order(order.ticker, datetime.datetime.now().strftime('%Y-%m-%d'), order.end.strftime('%H:%M:%S'),order.duration.strftime('%H:%M:%S'), order.pl, order.plpc)

                            latest_price = get_latest_price(order.ticker)
                            print(f"selling {order.quantity} of {order.ticker} at {latest_price}")
                            print(order)

        
        time.sleep(30)
                    
