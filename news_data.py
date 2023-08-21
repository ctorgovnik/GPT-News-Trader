
import matplotlib.pyplot as plt
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
import config


import requests
import time

def login():
    url = 'https://register.cnbc.com/'
    auth_key_url = 'https://www.cnbc.com/api/bedrock/authKey'
    login_route = '/auth/api/v3/signin'

    headers = {
        'User-Agent': config.cnbc_user,
        'origin': url,
        'referer': url + login_route
    }

    # Start a session
    s = requests.Session()

    # Get authKey
    auth_key_response = s.get(auth_key_url, headers=headers)
    auth_key_json = auth_key_response.json()
    authKey = auth_key_json.get('authKey')

    partnerId = auth_key_json.get('partnerId')

    # Create login payload
    login_payload = {
        'authKey': authKey,
        'password': config.cnbc_password,
        'pid': partnerId,
        'rememberMe': True,
        'uuid': config.cnbc_username,
    }

    while True:
        # Make the login POST request
        login_req = s.post('https://www.cnbc.com', headers=headers, json=login_payload)

        if login_req.status_code == 200:
            print("Login successful.")
            break
        else:
            print(f"Login failed with status code: {login_req.status_code}")
            retry_after = 60  # Wait for 60 seconds before re-trying
            print(f"Retrying after {retry_after} seconds...")
            time.sleep(retry_after)

    # Save the cookies for future requests
    cookies = login_req.cookies
    s.cookies = cookies

    return s

# # Example usage
# session = login()
# # Now use the 'session' object to make further requests.



def get_latest_article_link(session):
    url = "https://www.cnbc.com"  # replace with the actual URL
    response_latest = session.get(url)
    soup = BeautifulSoup(response_latest.text, 'html.parser')

    a_tag = soup.find('a', class_='LatestNews-headline')

    if a_tag is not None:
        href = a_tag['href']
        return href
    else:
        # Handle the case when 'a_tag' is None (no matching element found)
        print("Error: Could not find the latest article link.")
        return None


# get headline, key points, and body of article


def get_article_content(link, session):

    # response_article = requests.get(link)

    # response_article = requests.get(link)
    response_article = session.get(link)
    # if (True):
    #   # Get content from URL
    #   response_article = session.get(link)

    soup_article = BeautifulSoup(response_article.text, 'html.parser')

    # get article header
    article_headline_h1 = soup_article.find(
        'h1', class_='ArticleHeader-headline')

    article_headline = ''
    if article_headline_h1 is not None:
      article_headline =  article_headline_h1.text
    else:
      print('no article text found')
   

    print(article_headline)

    # Find the div containing the time
    article_time='N/A'
   # Find the div containing the time
    article_time_div = soup_article.find('div', class_='ArticleHeader-wrapperHeroNoImage ArticleHeader-wrapperHero ArticleHeader-wrapper ArticleHeader-wrapperNoImage')
    article_header_time_div = None
    article_time_tag = None
    

    if article_time_div is not None:
    #     # Find the time tag within the div
    #     article_header_time_div = article_time_div.find('div', class_='ArticleHeader-time')
    # else:
    #     print("no time header found")

    # if article_header_time_div is not None:

        article_time_tag = article_time_div.find('time', itemprop='datePublished')
        if article_time_tag is not None:
            # Get the text content of the <time> tag
            article_time = article_time_tag.text.strip()
            
            
            time_start_index = article_time.find('202')
            if time_start_index != -1:
                article_time = article_time[time_start_index + 4:]  # Extract from the character after the first space
                print("Published Time:", article_time)
            else:
                print("No time found.")

            print("Published Time:", article_time)
        else:
            print("No time found.")
            # else:
            #     print("No time header div found.")

    else:
        print ('article header not found')


    # get article key points
    article_key_points_div = soup_article.find(
        'div', class_='RenderKeyPoints-list')

    article_key_points = []

    if article_key_points_div is not None:
        article_key_points_li = article_key_points_div.find_all('li')
        article_key_points = [li.text for li in article_key_points_li]
    else:
        print("Could not find key points")

    print(article_key_points)

    # get tickers
    tickers = []
    article_tickers_ul = soup_article.find('ul', class_='RelatedQuotes-list')

    if article_tickers_ul is not None:
      tickers_li = article_tickers_ul.find_all('li', class_='QuoteItem-item')
      tickers = [ticker.text for ticker in tickers_li]
    else:
      print("could not find tickers")

    print(tickers)

    # get article body

    article_body_div = soup_article.find(
        'div', class_='ArticleBody-articleBody')
    # print(article_body_div)

    article_body = ""

    if article_body_div is not None:
        hidden_spans = article_body_div.find_all('span', hidden=True)
        if hidden_spans:
            for hidden_span in hidden_spans:
                if hidden_span.text not in article_body:
                    article_body += hidden_span.text
        else:
            # article_body_group_div = article_body_div.find(
            #     'div', class_='group')
            # if article_body_group_div is not None:
            #     article_body_p = article_body_group_div.find_all('p')
            #     article_body_list = [p.text for p in article_body_p]
            #     for par in article_body_list:
            #         if par not in article_body:
            #             article_body += par
            # Find all 'group' divs and extract text from paragraphs inside each div
            article_body_group_divs = article_body_div.find_all('div', class_='group')
            for group_div in article_body_group_divs:
                if group_div is not None:
                    article_body_p = group_div.find_all('p')
                    article_body_list = [p.text for p in article_body_p]
                    for par in article_body_list:
                        if par not in article_body:
                            article_body += par

    else:
        print("Could not find body of article")

    print(article_body)

    return article_headline, article_time, article_key_points, article_body, tickers


# session = login()
# article_link = get_latest_article_link(session)
# article_headline, article_time, article_key_points, article_text, tickers = get_article_content(
#     article_link, session)

# print('article time: ', article_time)
