import requests
from bs4 import BeautifulSoup

def scrape_friedrichsheim():
  items = []
  request_url = 'https://www.friedrichsheim-eg.de/category/freie-wohnungen/'
  response = requests.get(request_url, verify=False)
  parser = BeautifulSoup(response.content, 'html.parser')
  content = parser.find(id='main')
  if content:
    items_website = content.find_all('h2', class_='entry-title')
    for item in items_website:
      address = item.get_text() if item else None
      if address:
        items.append(address)
  return items

if __name__ == "__main__":
  print(', '.join(scrape_friedrichsheim())[:254])