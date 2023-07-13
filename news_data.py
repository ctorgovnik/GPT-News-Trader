
import matplotlib.pyplot as plt
import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_latest_article_link():
  url = "https://www.cnbc.com"  # replace with the actual URL
  response_latest = requests.get(url)
  soup = BeautifulSoup(response_latest.text, 'html.parser')

  a_tag = soup.find('a', class_='LatestNews-headline')

  href = a_tag['href']

  # print(href)
  return href

# get headline, key points, and body of article
def get_article_content(link):

  # response_article = requests.get(link)
  response_article = requests.get(link)
  soup_article = BeautifulSoup(response_article.text, 'html.parser')

  # get article header
  article_headline_h1 = soup_article.find('h1', class_ = 'ArticleHeader-headline')

  article_headline = article_headline_h1.text

  print(article_headline)

  # get article key points
  article_key_points_div = soup_article.find('div', class_ = 'RenderKeyPoints-list')

  article_key_points = []

  if article_key_points_div is not None:
      article_key_points_li = article_key_points_div.find_all('li')
      article_key_points = [li.text for li in article_key_points_li]
  else:
      print("Could not find key points")

  print(article_key_points)

  # get article body

  article_body_div = soup_article.find('div', class_ = 'ArticleBody-articleBody')



  article_body = ""

  if article_body_div is not None:
    article_body_group_div = article_body_div.find('div', class_='group')
    if article_body_group_div is not None:
      article_body_p = article_body_group_div.find_all('p')
      article_body_list = [p.text for p in article_body_p]
      for par in article_body_list:
        article_body = article_body + par
      
  else:
    print("Could not find body of article")

  print(article_body)

  return article_headline, article_key_points, article_body


article_link = get_latest_article_link()
article_headline, article_key_points, article_text = get_article_content(article_link)


