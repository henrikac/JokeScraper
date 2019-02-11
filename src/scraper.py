from bs4 import BeautifulSoup
import requests


jokes_scraped = 0
req = requests.get('https://www.rd.com/jokes/')
soup = BeautifulSoup(req.text, 'html.parser')

print(f'Status: {req.status_code}')

# get topics
topic_links = soup.select('.joke-tax > a')

for topic_link in topic_links:
  req = requests.get(topic_link['href'])
  soup = BeautifulSoup(req.text, 'html.parser')

  joke_links = [joke['href'] for joke in soup.find_all('a', class_='anchor-wrapper')]

  for joke_link in joke_links:
    req = requests.get(joke_link)
    soup = BeautifulSoup(req.text, 'html.parser')

    title = soup.find('div', class_='joke-title').get_text().strip()
    joke = soup.find('div', class_='joke-content').get_text().strip()

    with open(f'./jokes/{topic_link.get_text()}.txt', 'a') as file:
      file.write(f'{title}\n')
      file.write('-' * len(title))
      file.write(f'\n{joke}\n\n')

    jokes_scraped += 1

print(f'Jokes scraped: {jokes_scraped}')

