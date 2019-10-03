import requests
from bs4 import BeautifulSoup

def get_list_of_articles(number_of_pages):
    articles = []
    for i in range(number_of_pages):
        soup = BeautifulSoup(
            requests.get(f"https://www.presseportal.de/blaulicht/r/Baden-Baden/{i * 27}").text,
            "html.parser"
        )
        for article in soup.find_all("article", class_="news"):
            headline = article.find("h3", class_="news-headline-clamp").get_text()
            if (headline.startswith("POL-OG:") and "Baden-Baden" in headline):
                articles.append({
                    "url": article["data-url"],
                    "headline": headline
                })
    return articles

