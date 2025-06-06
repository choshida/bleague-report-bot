import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# チーム設定（琉球＝RSS、他2チーム＝HTML）
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

# RSS取得（User-Agent付き）
def scrape_from_rss(team_name, rss_url):
    logging.info(f"📡 {team_name}（RSS）")
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; BLeagueBot/1.0)"
    }

    try:
        response = requests.get(rss_url, headers=headers, timeout=10)
        if response.status_code != 200:
            logging.warning(f"{team_name} RSS取得失敗：{response.status_code}")
            return

        root = ET.fromstring(response.content)
        items = root.findall(".//item")
        logging.info(f"{team_name} RSS記事数: {len(items)}")

        for item in items[:5]:
            title = item.find("title").text
            pubDate = item.find("pubDate").text
            link = item.find("link").text
            print(f"{pubDate}｜{title}\n→ {link}\n")

    except Exception as e:
        logging.error(f"{team_name} RSS処理中にエラー：{e}")

# HTML取得
def scrape_from_html(team_name, config):
    logging.info(f"🏀 {team_name}（HTML）")
    try:
        res = requests.get(config["url"], timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.select(config["item_selector"])
        logging.info(f"{team_name} HTML記事数: {len(items)}")

        for item in items[:5]:
            title_tag = item.select_one(config["title_selector"])
            date_tag = item.select_one(config["date_selector"])
            link_tag = item.select_one(config["link_inside"])

            if title_tag and date_tag and link_tag:
                title = title_tag.get_text(strip=True)
                date = date_tag.get_text(strip=True)
                url = config["base_url"] + link_tag["href"]
                print(f"{date}｜{title}\n→ {url}\n")

    except Exception as e:
        logging.error(f"{team_name} HTML処理中にエラー：{e}")

# 実行本体
if __name__ == "__main__":
    for team_name, config in TEAMS.items():
        logging.info(f"[DEBUG] 処理中: {team_name}, type: {config.get('type')}")

        if config.get("type") == "rss":
            scrape_from_rss(team_name, config.get("rss_url", ""))
        elif config.get("type") == "scrape":
            scrape_from_html(team_name, config)
        else:
            logging.warning(f"{team_name} のtypeが不明または未設定")
