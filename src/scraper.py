from bs4 import BeautifulSoup
import concurrent.futures as cf
import requests
import time

from database import *


db.connect()
db.create_tables([Joke], safe=True)

headers = {
        'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)'
                        'AppleWebKit/537.36 (KHTML, like Gecko)'
                        'Chrome/50.0.2661.102 Safari/537.36')
        }
req = requests.get('https://www.rd.com/jokes/', headers=headers)
soup = BeautifulSoup(req.text, 'html.parser')


print(f'Status: {req.status_code}')

topic_links = soup.find_all('a', class_='tag-cloud-link')


def scrape_jokes(topic_link):
    req = requests.get(topic_link['href'], headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    return { "topic": topic_link.text, "jokes": soup }


with cf.ThreadPoolExecutor() as executor:
    topic_jokes = executor.map(scrape_jokes, topic_links)


for topic in topic_jokes:
    jokes = topic["jokes"].find_all(
        'article',
        class_=('pure-u-1 pure-u-sm-1-2'
                ' pure-u-lg-1-3 joke entry-card'
                ' category-card fixed-height')
    )

    for joke in jokes:
        title = joke.find('h3', class_='entry-title').text.strip()
        content = joke.find('div', class_='excerpt-wrapper').text.strip()

        add_joke(topic["topic"], title, content)


db.close()

