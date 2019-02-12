from bs4 import BeautifulSoup
import requests

from database import *


db.connect()
db.create_tables([Joke], safe=True)

jokes_scraped = 0
req = requests.get('https://www.rd.com/jokes/')
soup = BeautifulSoup(req.text, 'html.parser')


print(f'Status: {req.status_code}')

# get topics
topic_links = soup.find_all('a', class_='tag-cloud-link')

for topic_link in topic_links:
  req = requests.get(topic_link['href'])
  soup = BeautifulSoup(req.text, 'html.parser')

  jokes = soup.find_all('article', class_='joke entry-card fixed-height')

  for joke in jokes:
    title = joke.find('h2', class_='entry-title').get_text().strip()
    content = joke.find('div', class_='excerpt-wrapper').get_text().strip()

    add_joke(topic_link.get_text(), title, content)

    with open(f'./jokes/{topic_link.get_text()}.txt', 'a') as file:
      file.write(f'{title}\n')
      file.write('-' * len(title))
      file.write(f'\n{content}\n\n')

    jokes_scraped += 1

print(f'Jokes scraped: {jokes_scraped}')

db.close()

