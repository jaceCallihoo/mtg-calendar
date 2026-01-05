import requests
from bs4 import BeautifulSoup
import json

URL = "https://magic.wizards.com/en/news/mtg-arena"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")


articles = soup.find_all("a", href=True)

results = []
for article in articles:
    title_tag = article.find("h3")
    if title_tag:
        link = article["href"]
        if not link.startswith("http"):
            link = "https://magic.wizards.com" + link
        title = title_tag.text.strip()
        results.append({"title": title, "link": link})


with open("articles.json", "w") as f:
    json.dump(results, f, indent=2)

