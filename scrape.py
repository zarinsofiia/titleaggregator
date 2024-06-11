import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
from urllib.parse import urljoin
import json

url = 'https://www.theverge.com/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
articles = soup.find_all('a', class_='group hover:text-white')

headlines = []

for article in articles:
    aria_label = article.get('aria-label', '')

    if aria_label:
        title = aria_label
        href = article.get('href', '')

        link = urljoin(url, href)

        time_tag = article.find_next('time')
        pub_date_str = time_tag['datetime'] if time_tag else None

        if pub_date_str:
            pub_date = datetime.strptime(pub_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
            pub_date = pub_date.replace(tzinfo=timezone.utc)
            pub_date = pub_date + timedelta(hours=8)

            formatted_pub_date = pub_date.strftime('%b %d, %Y at %I:%M %p GMT+8')

            if pub_date >= datetime(2022, 1, 1, tzinfo=timezone.utc):
                headlines.append({
                    "title": title,
                    "link": link,
                    "pub_date": formatted_pub_date,
                    "aria_label": aria_label,
                    "href": href,
                })

headlines = [article for article in headlines if article['pub_date'] is not None]
headlines = sorted(headlines, key=lambda x: datetime.strptime(x['pub_date'], '%b %d, %Y at %I:%M %p GMT+8'), reverse=True)

with open('Article.json', 'w') as json_file:
    json.dump(headlines, json_file, indent=2)
