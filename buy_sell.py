import news_data
import prompttrainer as pt
from prompttrainer import NewsGpt
import time
import config

def buy_orders(bot, session, order_repo, category_repo, shared_order_list, order_lock, bot_lock):
    previous_link = ""

    while True:
        article_link = news_data.get_latest_article_link(session)
        if article_link is not None:
            print(article_link)
            if (article_link != previous_link):
                previous_link = article_link

                article_headline, article_time, _, article_text, _ = news_data.get_article_content(article_link, session)

                news_gpt = NewsGpt()
                news_gpt.categorize_article(article_text)

                if news_gpt.classification == "Breaking and Positive":
                    news_gpt.classify_breaking_positive(article_text, news_gpt.ticker)
                    if news_gpt.ticker != "N/A":
                        bot.buy_order(news_gpt.ticker, 1)
                        order_repo.add_order(article_headline, news_gpt.ticker, news_gpt.classification_breaking_positive, 1)
                        
                category_repo.add_classification(article_headline, news_gpt.ticker, news_gpt.classification, news_gpt.classification_breaking_positive, article_time, article_link)
                
                print(news_gpt)
                gpt_response = str(news_gpt)
                recipients = config.vonage_recipients
                message = pt.send_text_message(gpt_response, recipients)
            else:
                print("no new articles")
        else:
            print('article is none')

        time.sleep(300)


def sell_orders(bot, shared_order_list, order_lock, sell_lock, order_repo):
  return
