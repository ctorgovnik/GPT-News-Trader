
import matplotlib.pyplot as plt
import pandas as pd
import requests
from bs4 import BeautifulSoup







# # Start a session
# session = requests.Session()

# # Get login CSRF token (if applicable)
# login_page = session.get('https://www.cnbc.com/')
# login_page_soup = BeautifulSoup(login_page.text, 'html.parser')
# # csrf_token = login_page_soup.find('input', {'name': 'csrfToken'})['value'] # Adjust this based on the site's structure

# # Create payload
# payload = {
#     'email': 'cjt76@cornell.edu',
#     'password': 'Jess1ica*',
#     # 'csrfToken': csrf_token
# }

# # Post login
# post = session.post('https://www.cnbc.com/', data=payload)

def login():
    url = 'https://register.cnbc.com/'
    auth_key_url = 'https://www.cnbc.com/api/bedrock/authKey'
    login_route = '/auth/api/v3/signin'
    
    headers= {
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
        'password': '***', 
        'pid': partnerId,
        'rememberMe': False,
        'uuid': '***',
    }

    # Make the login POST request
    login_req = s.post('https://www.cnbc.com', headers=headers, json=login_payload)
    print(login_req.status_code)

    cookies = login_req.cookies
    print(cookies)

    return s

# def login():
#   url = 'https://register.cnbc.com'
#   url2 = 'https://www.cnbc.com'
#   login_route = '/auth/api/v3/signin'
#   headers= {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36', 'origin': url + login_route, 'referer': url + login_route}

#   s = requests.session()
#   # csrf_token = s.get(url).cookies['csrftoken']
#   login_payload = {"pid":33,"uuid":"cjt76@cornell.edu","password":"Jess1ica*","authKey":"0IrQbsZOiVCe5fbUzUpwsdATr4OB2HORIEcwHTHL9fay7Wy2xCkm0o6of94RRaDsH2hy5yEYwPuNJK1FS0sTzpbGrLtj7%2Fb5dq8dWR2o2as%3D","rememberMe":False}

#   login_req = s.post(url + login_route, headers=headers, data=login_payload)
#   print(login_req.status_code)

  # Start a session
  # session = requests.Session()

  # # Create payload
  # payload = {
  #     'pid': 33,  # This value may change; you need to find out where it comes from.
  #     'uuid': 'cjt76@cornell.edu',
  #     'password': 'Jess1ica*',
  #     'rememberMe': True,
  #     'authKey': '0IrQbsZOiVCe5fbUzUpwsdATr4OB2HORIEcwHTHL9fay7Wy2xCkm0o6of94RRaDsH2hy5yEYwPuNJK1FS0sTzpbGrLtj7%2Fb5dq8dWR2o2as%3D'  # This value may change; you need to find out where it comes from.
  # }

  # # Post login
  # response = session.post('https://register.cnbc.com/auth/api/v3/signin', json=payload)

  # # The response should indicate whether login was successful. You can print it to check.
  # print(response.json())





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
        print(par)
        article_body = article_body + par
      
  else:
    print("Could not find body of article")

  print(article_body)

  return article_headline, article_key_points, article_body

session = login()
article_link = get_latest_article_link(session)
article_headline, article_key_points, article_text = get_article_content('https://www.cnbc.com/2023/07/14/wells-fargo-beats-q2-expectations-heres-what-the-pros-are-saying.html', session)


