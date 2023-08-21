import news_data
import prompttrainer as pt
from prompttrainer import NewsGpt
import time
from order_repository import OrderRepository as order_repo
import yfinance as yf
from order_repository_sql import OrderRepositorySQL as order_sql
from category_repository import CategoryRepository as category_repo
from execution import ExecutionBot
from buy_sell import buy_orders
from sell import sell_orders

# from flask import Flask, request, jsonify

# app = Flask(__name__)

# article reader loop

previous_link = ""
ticker_list = []
session = news_data.login()

host = "localhost"
username = "root"
password = "Jess1ica"
database = "prompttrade"
order_repo = order_sql(host=host, user=username, password=password, database=database)
category_repo = category_repo(host=host, user=username, password=password, database=database)

bot = ExecutionBot()

while (True):

    article_link = news_data.get_latest_article_link(session)
    if article_link is not None:
            
        print(article_link)
        if (article_link != previous_link):
            previous_link = article_link

            article_headline, article_time, article_key_points, article_text, tickers = news_data.get_article_content(
                article_link, session)

            news_gpt = NewsGpt()

            news_gpt.categorize_article(article_text)

            if (news_gpt.classification == "Breaking and Positive"):
                # ticker_list.append(news_gpt.ticker)
                news_gpt.classify_breaking_positive(article_text, news_gpt.ticker)

                if (news_gpt.ticker!= "N/A"):
                    # need to treat multiple ticker case
                    # price = get_current_stock_price(news_gpt.ticker)
                    # order_repo.add_order(article_headline, news_gpt.ticker, news_gpt.classification_breaking_positive, 1, price)
                    bot.buy_order(news_gpt.ticker, 1)
                    order_repo.add_order(article_headline, news_gpt.ticker, news_gpt.classification_breaking_positive, 1)
                    # also have something to save the datafrae in case program crashes or stops



            category_repo.add_classification(article_headline, news_gpt.ticker, news_gpt.classification, news_gpt.classification_breaking_positive, article_time, article_link)
            print(news_gpt)
            gpt_response = str(news_gpt)
            recipients = ["19083070791", "19142261849"]
            message = pt.send_text_message(gpt_response, recipients)

        else:
            print("no new articles")
    else:
        print('article is none')

    time.sleep(300)



