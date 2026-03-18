import feedparser
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import requests
import os
from dotenv import load_dotenv
from rag_store import rag_store


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
        articles.append({
            "title": article.get("title", ""),
            "link": article.get("url", ""),
            "published": article.get("publishedAt", "")
        })
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
        all_news.append({
            "title": title,
            "published": published,
            "link": link
        })
        
    for item in google_news:
        title = item.get('title', '')
        published = item.get('published', '')
        link = item.get('link', '')
        all_news.append({
            "title": title,
            "published": published,
            "link": link
        })
        
    texts = []
    
    # Filter news articles to ensure they are from trustworthy sources and relevant to the stock ticker
    all_news = filter_news(all_news)
    all_news = all_news[:10]

    # Add all news articles to the RAG store for later retrieval
    for news in all_news:
        content = f"""
        Title: {news.get('title', '')}
        Description: {news.get('description', '')}
        Content: {news.get('content', '')}
        """
        texts.append(content)

    rag_store.add_documents(texts)

    return all_news

# Makes sure that the news articles are accurate and come from trustworthy sources
def filter_news(all_news):
    trusted_sources = ["bloomberg.com", "reuters.com", "wsj.com", "ft.com", "cnbc.com", "yahoo.com", "google.com"]
    filtered_news = []
    for news in all_news:
        link = news.get('link', '')
        if any(source in link for source in trusted_sources):
            filtered_news.append(news)
    return filtered_news

# Performs sentiment analysis on news articles related to the stock ticker
def sentiment_analysis(all_news):
    sia = SentimentIntensityAnalyzer()
    
    sentiments = []
    for news in all_news:
        title = news.get('title', '')
        sentiment = sia.polarity_scores(title)
        sentiments.append({
            "title": title,
            "sentiment": sentiment
        })
    
    return sentiments