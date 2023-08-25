import requests
import feedparser
import json
import time
from datetime import datetime

# Read RSS URLs from a text file
with open('rss_feeds.txt', 'r') as file:
    rss_feeds = [line.strip() for line in file.readlines()]

def fetch_feeds():
    all_entries = []

    for url in rss_feeds:
        response = requests.get(url)

        if response.status_code == 200:
            feed = feedparser.parse(response.content)

            for entry in feed.entries:
                all_entries.append({
                    'Title': entry.title,
                    'Link': entry.link,
                    'Published': entry.published
                })
        else:
            print(f'Failed to retrieve RSS feed from {url}')

    return all_entries

# Run the code every 30 minutes
while True:
    print('Fetching feeds...')
    data = fetch_feeds()

    # Create a file named with the current date
    date_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f'feeds_{date_str}.json'

    with open(filename, 'w') as file:
        json.dump(data, file)

    print(f'Successfully saved to {filename}')

    # Wait for 30 minutes before running again
    time.sleep(30 * 60)

