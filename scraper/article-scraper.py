import requests
import json
from bs4 import BeautifulSoup
import argparse

def to_camel_case(text):
    """Converts a string to camelCase."""
    words = text.split(' ')
    return words[0].lower() + ''.join(word.capitalize() for word in words[1:])

def scrape_event_schedule(html_content):
    """
    Scrapes the event schedule from the provided HTML content.

    Args:
        html_content: The HTML content of the article page.

    Returns:
        A dictionary containing the event schedule, or None if not found.
    """
    soup = BeautifulSoup(html_content, 'lxml')
    schedule_data = {}

    events_h2 = soup.find('h2', id='Events')
    if not events_h2:
        return None

    # Find all h3 tags that are within the event schedule section.
    all_h3s = soup.find_all('h3')
    schedule_h3s = []
    for h3 in all_h3s:
        # An h3 is in the event schedule section if its preceding h2 has id="Events".
        prev_h2 = h3.find_previous('h2')
        if prev_h2 and prev_h2.get('id') == 'Events':
            schedule_h3s.append(h3)

    for h3 in schedule_h3s:
        category_title = h3.get_text(strip=True)
        category_key = to_camel_case(category_title)
        
        # Find the ul that corresponds to this h3.
        ul = h3.find_next('ul')

        if ul and ul.find_previous('h3') == h3:
            events = []
            for li in ul.find_all('li'):
                # Use get_text() and then clean up whitespace to handle nested tags and <br>s gracefully.
                text = ' '.join(li.get_text().split())
                events.append(text)
            schedule_data[category_key] = events

    return {"eventSchedule": schedule_data}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape event schedule from a URL.')
    parser.add_argument('url', type=str, help='The URL of the article to scrape.')
    args = parser.parse_args()

    try:
        response = requests.get(args.url)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        exit(1)

    scraped_data = scrape_event_schedule(response.content)

    if scraped_data and scraped_data.get("eventSchedule"):
        print(json.dumps(scraped_data, indent=4, ensure_ascii=False))
    else:
        print("Could not find or scrape event schedule from the URL.")
