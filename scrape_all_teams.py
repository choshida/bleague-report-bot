import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

TEAMS = {
    "琉球ゴールデンキングス": {
        "type": "scrape",
        "url": "https://goldenkings.jp/news/",
        "base_url": "https://goldenkings.jp",
        "item_selector": ".newsList_item",
        "title_selector": ".newsList_title",
        "date_selector": ".newsList_date",
        "link_inside": "a"
    },
    "茨城ロボッツ": {
        "type": "scrape",
        "url": "https://www.ibarakirobots.win/news/",
        "base_url": "https://www.ibarakirobots.win",
        "item_selector": ".c-newsList__item",
        "title_selector": ".c-newsList__title",
        "date_selector": ".c-newsList__date",
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

def scrape_from_html(team_name, config):
    logging.info(f"\n🏀 {team_name}（HTML）")
    try:
        res = requests.get(config["url"], timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.select(config["item_selector"])
        logging.info(f"{team_name} HTML記事数: {len(items)}")

        if not items:
            logging.warning(f"{team_name} のニュース記事が取得できません")
            return

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

if __name__ == "__main__":
    for team_name, config in TEAMS.items():
        logging.info(f"[DEBUG] 処理中: {team_name}, type: {config.get('type')}")

        if config.get("type") == "scrape":
            scrape_from_html(team_name, config)
        else:
            logging.warning(f"{team_name} のtypeが不明または未設定")
