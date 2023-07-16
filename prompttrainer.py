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

    def __init__(self, ticker="N/A", classification="", description=""):
        self.ticker = ticker
        self.classification = classification
        self.description = description

    def categorize_article(self, article_text, tickers):
        self.ticker = tickers
        # Construct the prompt
        prompt = f'''
      Here is a news article: "{article_text}". The article is about these tickers: "{tickers}". \
      If the tickers is 'N/A' then the article doesn't mention any stocks. Please categorize it into one of the following categories:

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

    def classify_breaking_positive(self, article):
        return

    def __str__(self):
        return f"ticker: {self.ticker}\n\nclassification: {self.classification}\n\ndescription: {self.description}"


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


