import logging
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def scrape_with_screenshot():
    logging.info("🖼️ 琉球ゴールデンキングス - screenshot撮影中")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
            page.goto("https://goldenkings.jp/news/", timeout=20000)
            page.wait_for_load_state("networkidle")

            page.screenshot(path="screenshot.png", full_page=True)
            logging.info("✅ screenshot.png を保存しました")

            browser.close()

    except Exception as e:
        logging.error(f"スクリーンショット撮影に失敗：{e}")

if __name__ == "__main__":
    scrape_with_screenshot()
