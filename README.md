# 📈 Stock & News Email Alert System

This Python script fetches Apple's stock price and recent news articles. If the stock price changes beyond a set threshold, it sends an email notification with relevant news.

## 🚀 Features
- Fetches stock price data from Alpha Vantage 📊
- Retrieves recent news articles from NewsAPI 📰
- Sends email alerts only if the stock price change exceeds a threshold 📩
- Batch emails (one email with all news articles instead of multiple emails)
- Logging for debugging instead of `print()` statements 🛠️

## 🛠️ Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/stock-alert-system.git
   cd stock-news-alert
   ```
2. Create a `.env` file and add the following environment variables:
   ```env
   MY_EMAIL=your-email@email.com
   TO_EMAIL=recipient@email.com
   MY_PASSWORD=your-app-password
   STOCK_API_KEY=your-alphavantage-api-key
   NEWS_API_KEY=your-newsapi-key
   ```

## ▶️ Usage
Run the script with:
```sh
python main.py
```

## 📌 Requirements
- Python 3.7+
- `requests`, `python-dotenv`, `smtplib`

## 🛠️ Technologies Used
- Python
- Alpha Vantage API (Stock Data)
- NewsAPI (News Data)
- SMTP for email sending

## 👨‍💻 Created by [Tsaousidis](https://github.com/Tsaousidis)
🎉 Have fun! Let me know your thoughts and suggestions! 🎉