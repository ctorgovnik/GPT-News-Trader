import news_data
import prompttrainer as pt
from prompttrainer import NewsGpt
import time

# article reader loop

previous_link = ""
ticker_list = []
session = news_data.login()
while (True):

    article_link = news_data.get_latest_article_link(session)
    print(article_link)
    if (article_link != previous_link):
        previous_link = article_link

        article_headline, article_key_points, article_text = news_data.get_article_content(
            article_link, session)

        news_gpt = NewsGpt()

        news_gpt.categorize_article(article_text)

        print(news_gpt)

        gpt_response = str(news_gpt)
        recipients = ["19083070791", "19142261849"]
        message = pt.send_text_message(gpt_response, recipients)
        if (news_gpt.classification == "Breaking and Positive"):
            ticker_list.append(news_gpt.ticker)

    else:
        print("no new articles")
    time.sleep(900)
