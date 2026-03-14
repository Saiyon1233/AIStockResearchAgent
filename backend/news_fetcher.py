import feedparser

import requests
import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_news(news_url):

    response = requests.get(news_url)
    try:
        data = response.json()
    except Exception:
        return []
    articles = []
    for article in data.get("articles", []):
        articles.append(article.get("title", ""))
    return articles

def get_rss_news(feed_url):
    feed = feedparser.parse(feed_url)
    articles = []
    for entry in feed.entries:
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published
        })
    return articles

def get_all_news(ticker):

    # NewsAPI
    news_url = f"https://newsapi.org/v2/everything?q={ticker}&pageSize=5&apiKey={NEWS_API_KEY}"
    news = get_news(news_url)

    # Yahoo Finance
    yahoo_url = f"https://finance.yahoo.com/rss/headline?s={ticker}"
    yahoo_news = get_rss_news(yahoo_url)

    # Google News
    google_url = f"https://news.google.com/rss/search?q={ticker}"
    google_news = get_rss_news(google_url)

    # Combine and format news
    all_news = news
    for item in yahoo_news:
        title = item.get('title', '')
        published = item.get('published', '')
        link = item.get('link', '')
        all_news.append(f"{title} ({published}) - {link}")
    for item in google_news:
        title = item.get('title', '')
        published = item.get('published', '')
        link = item.get('link', '')
        all_news.append(f"{title} ({published}) - {link}")
    return all_news