
import matplotlib.pyplot as plt
import pandas as pd
import requests
from bs4 import BeautifulSoup


def login():
    url = 'https://register.cnbc.com/'
    auth_key_url = 'https://www.cnbc.com/api/bedrock/authKey'
    login_route = '/auth/api/v3/signin'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
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
        'password': 'Jess1ica*',
        'pid': partnerId,
        'rememberMe': False,
        'uuid': 'cjt76@cornell.edu',
    }

    # Make the login POST request
    login_req = s.post('https://www.cnbc.com',
                       headers=headers, json=login_payload)
    print(login_req.status_code)

    cookies = login_req.cookies
    print(cookies)

    return s


def get_latest_article_link(session):

    url = "https://www.cnbc.com"  # replace with the actual URL
    # response_latest = requests.get(url)
    response_latest = session.get(url)
    soup = BeautifulSoup(response_latest.text, 'html.parser')

    a_tag = soup.find('a', class_='LatestNews-headline')

    href = a_tag['href']

    # print(href)
    return href

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

    article_headline = article_headline_h1.text

    print(article_headline)

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
            article_body_group_div = article_body_div.find(
                'div', class_='group')
            if article_body_group_div is not None:
                article_body_p = article_body_group_div.find_all('p')
                article_body_list = [p.text for p in article_body_p]
                for par in article_body_list:
                    if par not in article_body:
                        article_body += par

    else:
        print("Could not find body of article")

    print(article_body)

    return article_headline, article_key_points, article_body, tickers


session = login()
article_link = get_latest_article_link(session)
article_headline, article_key_points, article_text, tickers = get_article_content(
    article_link, session)
