import requests
import json
from bs4 import BeautifulSoup
import argparse

def scrape_article(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

    soup = BeautifulSoup(response.content, 'lxml')

    article_title_element = soup.find('h1', class_='css-om3e2 css-EsYAb')
    article_title = article_title_element.get_text(strip=True) if article_title_element else 'No title found'

    article_date_element = soup.find('time')
    article_date = article_date_element.get_text(strip=True) if article_date_element else 'No date found'

    article_content = ''
    content_div = soup.find('div', class_='article-body css-cvK8p')
    if content_div:
        article_content = content_div.get_text(separator='\n', strip=True)
    else:
        article_content = 'No content found'


    data = {
        'url': url,
        'title': article_title,
        'date': article_date,
        'content': article_content.strip()
    }

    return data

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape an article from a URL.')
    parser.add_argument('url', type=str, help='The URL of the article to scrape.')
    args = parser.parse_args()

    scraped_data = scrape_article(args.url)

    if scraped_data:
        print(json.dumps(scraped_data, indent=2))
