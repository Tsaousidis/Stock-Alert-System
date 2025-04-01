
import requests
import os
from dotenv import load_dotenv
import smtplib
from datetime import datetime

load_dotenv()

TICKER = "TSLA"
ISSUER = "Tesla Inc"
THRESHOLD_PERCENT = 1.0

MY_EMAIL = os.getenv("MY_EMAIL") # Change this with your email
TO_EMAIL = os.getenv("TO_EMAIL") # Change this to the recipient's email
MY_PASSWORD = os.getenv("MY_PASSWORD") # Change this with your app password you've created in your email 

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = os.getenv("STOCK_API_KEY")
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def main():
    prices = get_closing_price(TICKER)

    # Get the most recent two trading days
    available_dates = sorted(prices.keys(), reverse=True)[:2]

    if len(available_dates) < 2:
        print("❌ Not enough data available.")
        return        

    latest_closing_price = float(prices[available_dates[0]]["4. close"])
    previous_closing_price = float(prices[available_dates[1]]['4. close'])
    change = get_difference(previous_closing_price, latest_closing_price)

    if change["percentage"] >= THRESHOLD_PERCENT:
        news = get_news(ISSUER)

        if not news:
            print("⚠️ No relevant news found.")
            return

        for article in news:
            emoji = "🔺" if change["price_went_up"] else "🔻"
            subject = f"{TICKER}: {emoji}{change['difference']:.2f}% Change"
            body = "\n\n".join(
                [f"📰 {article['title']}\n{article['description']}" for article in news]
            )
            send_email(subject, body)


def get_closing_price(ticker):
    stock_parameters = {
        "function": "TIME_SERIES_DAILY",
        "symbol": ticker,
        "apikey": STOCK_API_KEY,
    }

    response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
    response.raise_for_status()
    data = response.json()

    return data.get("Time Series (Daily)", {})

def get_difference(previous_price, latest_price):
    difference = abs(previous_price - latest_price)
    price_went_up = latest_price > previous_price
    diff_percent = round((difference * 100) / previous_price, 2)

    return {'difference': difference, 'price_went_up': price_went_up, 'percentage': diff_percent}

def get_news(issuer):
    news_parameters = {
        "qInTitle": issuer,
        "apiKey": NEWS_API_KEY,
        "sortBy": "popularity"
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    news_response.raise_for_status()
    articles = news_response.json().get("articles", [])

    return articles[:3] if articles else []
 
def send_email(subject, body):
    try:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            msg = f"Subject: {subject}\r\n\r\n{body}"

            connection.sendmail(from_addr=MY_EMAIL, to_addrs=TO_EMAIL, msg=msg.encode("utf-8"))
        print(f"✅ Email sent successfully to {TO_EMAIL}")
    except smtplib.SMTPException as e:
        print(f"❌ Failed to send email: {e}")

if __name__ == "__main__":
    main()