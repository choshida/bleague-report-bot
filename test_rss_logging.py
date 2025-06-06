import feedparser
import logging

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')

team_name = "琉球ゴールデンキングス"
rss_url = "https://goldenkings.jp/news/rss.xml"

logging.info(f"{team_name} のRSSを読み込み中...")

feed = feedparser.parse(rss_url)
logging.info(f"RSS件数: {len(feed.entries)}")

for entry in feed.entries[:3]:
    logging.info(f"{entry.get('published', '日付不明')}｜{entry.get('title', 'タイトル不明')}")
