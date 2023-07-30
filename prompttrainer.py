import news_data
import os
import openai
import json
# from twilio.rest import Client
import vonage
import time


openai.api_key = "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"


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.0,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


class NewsGpt:

    def __init__(self, ticker="N/A", classification="", description="", classification_breaking_positive = "N/A", description_breaking_positive= "N/A"):
        self.ticker = ticker
        self.classification = classification
        self.description = description
        self.classification_breaking_positive = classification_breaking_positive
        self.description_breaking_positive = description_breaking_positive

    def categorize_article(self, article_text):
        # self.ticker = tickers
        # Construct the prompt
        prompt = f'''
      Here is a news article: "{article_text}". Find the ticker or tickers of the article. \
      Sometimes they will be in ticker abbrevation or it will name the full company, but always put it in ticker format. \
      If there is no ticker named then return 'N/A' for ticker. Please categorize it into one of the following categories:

      1. "Breaking and Positive" - The news is just out, it's the first or one of the first articles on \
      the subject, and the content is likely to cause the stock price to increase. \
      The market might not have fully absorbed the news yet, providing a potential buying opportunity.\
      If the article does not mention a significant increase in the stock price, it is more likely to be in this \
      category.
      
      2. "Stale and Positive" - The news is not fresh anymore, it's been some hours (or longer) since the \
      story broke, but the content is positive. The information is likely already reflected in the stock price, \
      and it might not be a new buying opportunity. If the article mentions that the stock price has already \
      increased significantly, it is more likely to be in this category.
      
      3. "Breaking and Negative" - The news is just out, it's the first or one of the first articles on the subject,\
      and the content is likely to cause the stock price to decrease. The market might not have fully absorbed the\
      news yet, providing a potential selling opportunity. If the article does not mention a significant decrease \
      in the stock price, it is more likely to be in this category.
      
      4. "Stale and Negative" - The news is not fresh anymore, it's been some hours (or longer) \
      since the story broke, and the content is negative. The information is likely already reflected in the \
      stock price, and it might not be a new selling opportunity. If the article mentions that the stock price \
      has already decreased significantly, it is more likely to be in this category.

      5. "Other" - The article does not fit into any of the listed categories.

      Format your response as a JSON object with the ticker the article is about (or list of tickers if needed) with "ticker" as the key,\
      category classification with key "classification", and brief description of what happened and why this classification with key "description".
        
      If you cannot find a stock ticker, also mention in the decription that the article does not mention any specific stocks, and return "N/A" for "ticker".
      '''

        response = get_completion(prompt)

        response_json = json.loads(response)

        # Extract values from the JSON
        self.ticker = response_json["ticker"]
        self.classification = response_json["classification"]
        self.description = response_json["description"]
        # return response

    def classify_breaking_positive(self, article, ticker):

        prompt = f'''
      Here is a news article: "{article}". The article is about these ticker(s): "{ticker} \
      We have already classified this article as 'Breaking and Positive'. Now, I want you to further classify it in one of the following:

      1. "Bank Price Upgrade" - A bank has just come out and said they are raising their price target for this stock \
        or they are saying they see huge potential for it in the future.
      
      2. "Major Partnership or Collaboration" - The article talks about a significant partnership or collaboration  \
      that could boost the company's growth prospects and market presence. This could be a rumor too.
      
      3. "Innovative Technology Advancement" - The news covers a groundbreaking technological advancement made by the company, \
         signaling potential growth and competitive advantage.
      
      4. "Industry Recognition or Awards" - The news highlights that the company has received notable industry recognition or awards, \
         enhancing its reputation and credibility.

      5. "Positive Regulatory or Legal Outcome" - The article discusses a favorable regulatory decision \
         or legal outcome that could positively impact the company's operations. This could be overcoming a legal obstacle as well.

      6. "Expansion into New Markets" - The article covers the company's successful expansion into new markets, \
         broadening its customer base and revenue streams.
      
      7. "Other" - The article does not fit into any of the listed categories.

      Format your response as a JSON object with category classification with key "classification_breaking_positive", \
      and brief description of why this classification with key "description_breaking_positive".
        
      '''

        response = get_completion(prompt)

        response_json = json.loads(response)

        # Extract values from the JSON
        
        self.classification_breaking_positive = response_json["classification_breaking_positive"]
        self.description_breaking_positive = response_json["description_breaking_positive"]

    def __str__(self):
        return f"""ticker: {self.ticker}\n\nclassification: {self.classification}\n\ndescription: {self.description} \n\n\n
        breaking/positive classification: {self.description_breaking_positive} \n\n breaking/positive decription: {self.description_breaking_positive}"""


def send_text_message(message, recipients):

    client = vonage.Client(key="25dad562", secret="m4vHCnYMHJIQ4whC")
    sms = vonage.Sms(client)

    for recipient in recipients:
        responseData = sms.send_message(
            {
                "from": "15703306259",
                "to": recipient,
                "text": message,
            }
        )

        if responseData["messages"][0]["status"] == "0":
            print("Message sent successfully.")
        else:
            print(
                f"Message failed with error: {responseData['messages'][0]['error-text']}")


