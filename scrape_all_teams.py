import requests
from bs4 import BeautifulSoup

# チームごとの設定（セレクタは2025年6月時点で確認済み）
TEAMS = {
    "琉球ゴールデンキングス": {
        "url": "https://goldenkings.jp/news/",
        "base_url": "https://goldenkings.jp",
        "item_selector": "ul.list > li",
        "title_selector": ".title",
        "date_selector": ".date",
        "link_inside": "a"
    },
    "茨城ロボッツ": {
        "url": "https://www.ibarakirobots.win/news/",
        "base_url": "https://www.ibarakirobots.win",
        "item_selector": ".news-item",
        "title_selector": ".title",
        "date_selector": ".date",
        "link_inside": "a"
    },
    "信州ブレイブウォリアーズ": {
        "url": "https://www.b-warriors.net/news/",
        "base_url": "https://www.b-warriors.net",
        "item_selector": "ul.news__list > li",
        "title_selector": ".news__list-title",
        "date_selector": ".news__list-date",
        "link_inside": "a"
    }
}

def scrape_team(name, config):
    try:
        res = requests.get(config["url"], timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.select(config["item_selector"])[:5]

        print(f"🏀 {name}")
        if not items:
            print("⚠️ ニュース項目が見つかりませんでした\n")
            return

        hit = 0
        for item in items:
            title_tag = item.select_one(config["title_selector"])
            date_tag = item.select_one(config["date_selector"])
            link_tag = item.select_one(config["link_inside"])

            if title_tag and date_tag and link_tag:
                title = title_tag.get_text(strip=True)
                date = date_tag.get_text(strip=True)
                url = config["base_url"] + link_tag["href"]

                print(f"{date}｜{title}")
                print(f"→ {url}\n")
                hit += 1

        if hit == 0:
            print("⚠️ セレクタに一致する記事がありませんでした\n")

        print("-" * 40)

    except Exception as e:
        print(f"[ERROR] {name} の取得に失敗しました：{e}")

if __name__ == "__main__":
    for team, config in TEAMS.items():
        scrape_team(team, config)
