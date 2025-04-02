
import requests
import os
import logging
from dotenv import load_dotenv
import smtplib
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables from .env file
load_dotenv()

# Stock and news configuration
TICKER = "AAPL"
ISSUER = "Apple Inc"
THRESHOLD_PERCENT = 5.0 # Percentage change threshold to trigger email

# Email credentials (loaded from environment variables)
MY_EMAIL = os.getenv("MY_EMAIL") # Change this with your email
TO_EMAIL = os.getenv("TO_EMAIL") # Change this to the recipient's email
MY_PASSWORD = os.getenv("MY_PASSWORD") # Change this with your app password you've created in your email 

# API Endpoints and Keys (loaded from environment variables)
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = os.getenv("STOCK_API_KEY")
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def main():
    """Main function to check stock price change and send relevant news via email."""
    prices = get_closing_price(TICKER)

    # Get the most recent two trading days
    available_dates = sorted(prices.keys(), reverse=True)[:2]

    if len(available_dates) < 2:
        logging.warning("❌ Not enough data available.")
        return        

    latest_closing_price = float(prices[available_dates[0]]["4. close"])
    previous_closing_price = float(prices[available_dates[1]]['4. close'])
    change = get_difference(previous_closing_price, latest_closing_price)

    # If stock price change exceeds threshold, fetch news and send email
    if change["percentage"] >= THRESHOLD_PERCENT:
        news = get_news(ISSUER)

        if not news:
            logging.warning("⚠️ No relevant news found.")
            return
        
        emoji = "🔺" if change["price_went_up"] else "🔻"
        subject = f"{TICKER}: {emoji}{change['difference']:.2f}% Change"

        # Create email body with all articles
        body = "\n\n".join([
            f"📰 {article.get('title', 'No Title Available')}\n"
            f"{article.get('description', 'No description available.')}"
            for article in news
        ])
        
        send_email(subject, body)

def get_closing_price(ticker):
    """Fetches the latest daily closing prices for the given stock ticker."""
    stock_parameters = {
        "function": "TIME_SERIES_DAILY",
        "symbol": ticker,
        "apikey": STOCK_API_KEY,
    }

    try:
        response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
        response.raise_for_status()
        data = response.json()
        return data.get("Time Series (Daily)", {})
    except requests.RequestException as e:
        logging.error(f"❌ Error fetching stock data: {e}")
        return {}

def get_difference(previous_price, latest_price):
    """Calculates the absolute and percentage difference between two prices."""
    difference = abs(previous_price - latest_price)
    price_went_up = latest_price > previous_price
    diff_percent = round((difference * 100) / previous_price, 2)

    return {'difference': difference, 'price_went_up': price_went_up, 'percentage': diff_percent}

def get_news(issuer):
    """Fetches the top 3 most relevant news articles based on the company name."""
    news_parameters = {
        "qInTitle": issuer,
        "apiKey": NEWS_API_KEY,
        "sortBy": "popularity"
    }

    try:
        news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
        news_response.raise_for_status()
        articles = news_response.json().get("articles", [])
        return articles[:3] if articles else []
    except requests.RequestException as e:
        logging.error(f"❌ Error fetching news: {e}")
        return []
 
def send_email(subject, body):
    """Sends an email notification with the given subject and body."""
    try:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            msg = f"Subject: {subject}\r\n\r\n{body}"

            connection.sendmail(from_addr=MY_EMAIL, to_addrs=TO_EMAIL, msg=msg.encode("utf-8"))
        logging.info(f"✅ Email sent successfully to {TO_EMAIL}")
    except smtplib.SMTPException as e:
        logging.error(f"❌ Failed to send email: {e}")

# Run the script
if __name__ == "__main__":
    main()