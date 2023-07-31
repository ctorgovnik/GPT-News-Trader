import news_data
import prompttrainer as pt
from prompttrainer import NewsGpt
import time
from order_repository import OrderRepository as order_repo
import yfinance as yf
from order_repository_sql import OrderRepositorySQL as order_sql
from category_repository import CategoryRepository as category_repo

# article reader loop

previous_link = ""
ticker_list = []
session = news_data.login()

host = "localhost"
username = "root"
password = "***"
database = "prompttrade"
order_repo = order_sql(host=host, user=username, password=password, database=database)
category_repo = category_repo(host=host, user=username, password=password, database=database)

order_repo.create_orders_table()
category_repo.create_classification_table()

while (True):

    article_link = news_data.get_latest_article_link(session)
    print(article_link)
    if (article_link != previous_link):
        previous_link = article_link

        article_headline, article_key_points, article_text, tickers = news_data.get_article_content(
            article_link, session)

        news_gpt = NewsGpt()

        news_gpt.categorize_article(article_text)

        print(news_gpt)

        gpt_response = str(news_gpt)
        recipients = ["19083070791", "19142261849"]
        message = pt.send_text_message(gpt_response, recipients)

        category_repo.add_classification(article_headline, news_gpt.ticker, news_gpt.classification, news_gpt.classification_breaking_positive)

        if (news_gpt.classification == "Breaking and Positive"):
            # ticker_list.append(news_gpt.ticker)
            news_gpt.description_breaking_positive(article_text, news_gpt.ticker)

            if (news_gpt.ticker!= "N/A"):
                # need to treat multiple ticker case
                price = get_current_stock_price(news_gpt.ticker)
                # order_repo.add_order(article_headline, news_gpt.ticker, news_gpt.classification_breaking_positive, 1, price)
                order_repo.add_order(article_headline, news_gpt.ticker, news_gpt.classification_breaking_positive, 1, price)
                # also have something to save the datafrae in case program crashes or stops

    else:
        print("no new articles")
    time.sleep(900)


    def get_current_stock_price(self, ticker):
        try:
            # Fetch current stock price using yfinance
            stock_data = yf.download(ticker, period='1d', interval='1m')
            current_price = stock_data.iloc[-1]['Close']
            return current_price
        except Exception as e:
            print(f"Error fetching stock price: {e}")
            return None
