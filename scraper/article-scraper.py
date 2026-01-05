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
    parser = argparse.ArgumentParser(description='Scrape event schedule from an HTML file.')
    parser.add_argument('input_file', type=str, nargs='?', default='article.html',
                        help='The HTML file to scrape (default: article.html).')
    parser.add_argument('output_file', type=str, nargs='?', default='output.json',
                        help='The output JSON file (default: output.json).')
    args = parser.parse_args()

    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"Error: Input file '{args.input_file}' not found.")
        exit(1)

    scraped_data = scrape_event_schedule(html_content)

    if scraped_data and scraped_data.get("eventSchedule"):
        with open(args.output_file, 'w', encoding='utf-8') as f:
            json.dump(scraped_data, f, indent=4, ensure_ascii=False)
        print(f"Scraped data saved to '{args.output_file}'")
    else:
        print("Could not find or scrape event schedule from the input file.")
