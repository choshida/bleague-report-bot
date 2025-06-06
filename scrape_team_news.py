import requests
from bs4 import BeautifulSoup

def scrape_ryukyu():
    url = "https://goldenkings.jp/news/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    news_list = []
    articles = soup.select(".list-item")[:5]  # 最新5件

    for a in articles:
        title_tag = a.select_one(".list-title")
        date_tag = a.select_one(".list-date")
        link_tag = a.find("a")

        if title_tag and date_tag and link_tag:
            news = {
                "title": title_tag.get_text(strip=True),
                "date": date_tag.get_text(strip=True),
                "url": "https://goldenkings.jp" + link_tag["href"]
            }
            news_list.append(news)

    return news_list

if __name__ == "__main__":
    for n in scrape_ryukyu():
        print(f"{n['date']}｜{n['title']}")
        print(f"→ {n['url']}\n")
