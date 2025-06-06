import logging
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def scrape_ryukyu_with_playwright():
    logging.info("🏀 琉球ゴールデンキングス（Playwright）")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://goldenkings.jp/news/", timeout=20000)
            page.wait_for_load_state("networkidle")
            page.wait_for_selector(".newsList_item", timeout=30000)

            items = page.query_selector_all(".newsList_item")[:5]
            logging.info(f"記事数: {len(items)}")

            for item in items:
                title = item.query_selector(".newsList_title").inner_text().strip()
                date = item.query_selector(".newsList_date").inner_text().strip()
                link = item.query_selector("a").get_attribute("href")
                full_url = f"https://goldenkings.jp{link}"
                print(f"{date}｜{title}\n→ {full_url}\n")

            browser.close()

    except Exception as e:
        logging.error(f"Playwrightでの取得に失敗：{e}")

if __name__ == "__main__":
    scrape_ryukyu_with_playwright()
