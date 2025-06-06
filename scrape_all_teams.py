import requests
import feedparser
from bs4 import BeautifulSoup

# チーム設定：typeに応じてrss or scrapeを使い分け
TEAMS = {
    "琉球ゴールデンキングス": {
        "type": "rss",
        "rss_url": "https://goldenkings.jp/news/rss.xml"
    },
    "茨城ロボッツ": {
        "type": "scrape",
        "url": "https://www.ibarakirobots.win/news/",
        "base_url": "https://www.ibarakirobots.win",
        "item_selector": ".news-item",
        "title_selector": ".title",
        "date_selector": ".date",
        "link_inside": "a"
    },
    "信州ブレイブウォリアーズ": {
        "type": "scrape",
        "url": "https://www.b-warriors.net/news/",
        "base_url": "https://www.b-warriors.net",
        "item_selector": "ul.news__list > li",
        "title_selector": ".news__list-title",
        "date_selector": ".news__list-date",
        "link_inside": "a"
    }
}

# RSS方式
def scrape_from_rss(team_name, rss_url):
    print(f"\n📡 {team_name}（RSS）")
    print("-" * 40)
    feed = feedparser.parse(rss_url)
    if not feed.entries:
        print("⚠️ RSSが空です")
    for entry in feed.entries[:5]:
        published = entry.get("published", "日付不明")
        title = entry.get("title", "タイトル不明")
        link = entry.get("link", "URL不明")
        print(f"{published}｜{title}")
        print(f"→ {link}\n")

# HTMLスクレイピング方式
def scrape_from_html(team_name, config):
    print(f"\n🏀 {team_name}（HTML）")
    print("-" * 40)
    try:
        res = requests.get(config["url"], timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.select(config["item_selector"])
        print(f"🔍 要素数: {len(items)}")

        if not items:
            print("⚠️ ニュース項目が見つかりません")
            return

        for item in items[:5]:
            title_tag = item.select_one(config["title_selector"])
            date_tag = item.select_one(config["date_selector"])
            link_tag = item.select_one(config["link_inside"])

            if title_tag and date_tag and link_tag:
                title = title_tag.get_text(strip=True)
                date = date_tag.get_text(strip=True)
                url = config["base_url"] + link_tag["href"]

                print(f"{date}｜{title}")
                print(f"→ {url}\n")

    except Exception as e:
        print(f"[ERROR] {team_name} の取得に失敗：{e}")

# 実行エントリーポイント
if __name__ == "__main__":
    for team_name, config in TEAMS.items():
        if config["type"] == "rss":
            scrape_from_rss(team_name, config["rss_url"])
        elif config["type"] == "scrape":
            scrape_from_html(team_name, config)
        else:
            print(f"⚠️ {team_name} のtype設定が不明です")
