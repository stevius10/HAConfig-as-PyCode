import requests
from bs4 import BeautifulSoup

def scrape_wbm():
  items = []
  request_url = 'https://www.wbm.de/wohnungen-berlin/angebote/'
  response = requests.get(request_url, verify=False)
  parser = BeautifulSoup(response.content, 'html.parser')
  content = parser.find(id='content')
  if content:
    items_website = content.find_all(class_='immo-element')
    for item in items_website:
      address = item.find(class_='address').get_text() if item.find(class_='address') else None
      area = item.find(class_='area').get_text().lower() if item.find(class_='area') else None
      rent = item.find(class_='main-property-rent').get_text() if item.find(class_='main-property-rent') else None
      size = item.find(class_='main-property-size').get_text() if item.find(class_='main-property-size') else None
      rooms = item.find(class_='main-property-rooms').get_text() if item.find(class_='main-property-rooms') else None
      details = item.find(class_='check-property-list').get_text() if item.find(class_='check-property-list') else None
      if address and 'WBS' not in details and any(a in area for a in ['friedrichshain', 'kreuzberg', 'schöneberg', 'neukölln']):
        items.append(f"{address} ({rooms}/{size}, {rent})")
  return items

if __name__ == "__main__":
  print(', '.join(scrape_wbm())[:254])