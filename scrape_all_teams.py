import logging
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def scrape_ryukyu_stable():
    logging.info("🏀 琉球ゴールデンキングス（Playwright）")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
            page.goto("https://goldenkings.jp/news/", timeout=20000)
            page.wait_for_load_state("networkidle")
            page.mouse.wheel(0, 3000)

            # 要素が存在するかに関係なく強制取得（ログも出力）
            items = page.query_selector_all(".newsList_item")
            logging.info(f"取得できた.newsList_item数: {len(items)}")

            for item in items[:5]:
                try:
                    title = item.query_selector(".newsList_title").inner_text().strip()
                    date = item.query_selector(".newsList_date").inner_text().strip()
                    link = item.query_selector("a").get_attribute("href")
                    full_url = f"https://goldenkings.jp{link}"
                    print(f"{date}｜{title}\n→ {full_url}\n")
                except Exception as inner_e:
                    logging.warning(f"要素処理エラー：{inner_e}")

            browser.close()

    except Exception as e:
        logging.error(f"Playwrightでの取得に失敗：{e}")

if __name__ == "__main__":
    scrape_ryukyu_stable()
