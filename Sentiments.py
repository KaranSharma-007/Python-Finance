import requests
from bs4 import BeautifulSoup
from textblob import TextBlob

# Function to get market news
def get_google_news(Query, Date):
    date = Date.strftime('%d %b %Y')

    # Set headers to mimic a real browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Google News RSS Feed URL
    url = f"https://news.google.com/rss/search?q={Query}+{date}&hl=en-IN&gl=IN&ceid=IN:en"

    # Fetch the RSS feed
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Error fetching news feed.")
        return

    # Parse the feed using BeautifulSoup
    soup = BeautifulSoup(response.content, "xml")
    items = soup.find_all("item")

    print(f"Latest news for {Query} as of {date}:\n")
    articles = []
    
    for item in items:   
        title = item.title.text
        published = item.pubDate.text
        if Query in title and date in published:
            articles.append(title)
            print(f"Title: {title}")
            print(f"Published: {published}")
            print("-" * 50)
    return articles

# Function to calculate aggregated sentiment score using TextBlob
def get_aggregated_sentiment(articles):
    sentiment_scores = []
    for article in articles:
        polarity, subjectivity = TextBlob(article).sentiment
        score = polarity*(1 - subjectivity)
        sentiment_scores.append(score)
        if score>0:
            res = "Positve"
        elif score == 0:
            res = "Neutral"
        else:
            res = "Negative"
        print(f'{res}:- {article}')

    if sum(sentiment_scores) == 0:
        return 0
    return sum(sentiment_scores) / len(sentiment_scores)