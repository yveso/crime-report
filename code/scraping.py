import requests
from bs4 import BeautifulSoup
from datetime import datetime


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


def get_article(url):
    soup = BeautifulSoup(
        requests.get(url).text,
        "html.parser"
    )
    div_card = soup.find("div", class_="card")
    sidebar = soup.find("div", class_="story-linkbox")
    
    date_text = div_card.find("p", class_="date").get_text()
    publish_date = datetime.strptime(date_text, "%d.%m.%Y – %H:%M")
    
    publisher = div_card.find("p", class_="customer").get_text().strip()
    
    headline_raw = div_card.find("h1").get_text()
    headline = "".join(headline_raw.split(":")[1:]).strip()
    
    content = div_card.find_all("p")[3].get_text().strip()
    
    location_tags = list(filter(
        lambda tag: tag != "Baden-Württemberg",
        [tag.get_text() for tag in sidebar.find_all("ul", class_="tags")[0].contents]
    ))
    
    topic_tags = list(filter(
        lambda tag: tag not in ["POL", "Polizei", "Polizei Baden-Württemberg"],
        [tag.get_text() for tag in sidebar.find_all("ul", class_="tags")[1].contents]
    ))
    
    return {
        "url": url,
        "publish_date": publish_date,
        "publisher": publisher,
        "headline": headline,
        "content": content,
        "location_tags": location_tags,
        "topic_tags": topic_tags
    }

