import feedparser
from datetime import datetime

def get_bleague_rss():
    rss_url = "https://www.bleague.jp/news/rss/"
    feed = feedparser.parse(rss_url)
    results = []

    for entry in feed.entries:
        results.append({
            "title": entry.title,
            "url": entry.link,
            "summary": entry.get("summary", ""),
            "published": entry.get("published", ""),
            "published_dt": datetime(*entry.published_parsed[:6])
        })

    return results

if __name__ == "__main__":
    news_list = get_bleague_rss()
    for news in news_list[:5]:
        print(f"{news['published_dt'].strftime('%Y-%m-%d %H:%M')}｜{news['title']}")
        print(f"→ {news['url']}\n")
