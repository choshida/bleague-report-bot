from playwright.sync_api import sync_playwright

def inspect_iframes():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
        page.goto("https://goldenkings.jp/news/", timeout=20000)
        page.wait_for_load_state("networkidle")

        frames = page.frames
        print(f"🧭 フレーム数: {len(frames)}")

        for i, frame in enumerate(frames):
            print(f"\n[FRAME {i}] URL: {frame.url}")
            try:
                items = frame.query_selector_all(".newsList_item")
                print(f"→ .newsList_item 要素数: {len(items)}")
            except Exception as e:
                print(f"⚠️ フレーム内取得エラー: {e}")

        browser.close()

if __name__ == "__main__":
    inspect_iframes()
