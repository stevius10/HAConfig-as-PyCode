import requests
from bs4 import BeautifulSoup

def scrape_pollenflug():
  items = []
  request_url = 'https://www.gesundheit.de/biowetter/berlin-id213016/#:~:text=Biowetter%20Berlin%20(Region),-Gestern&text=Die%20derzeitige%20Wetterlage%20beeinflusst%20Arbeitsleistung,und%20Stoffwechsel%20laufen%20beschleunigt%20ab.'
  response = requests.get(request_url, verify=False)
  parser = BeautifulSoup(response.content, 'html.parser')
  content = parser.find(class_='article')
  if content:
    items_website = content.find_all(class_='table-ps')[2].find_all('tr')
    for item in items_website:
      name = item.select('td[data-title*=":"]')[0].get_text(strip=True) if item.select('td[data-title*=":"]') else None
      value = item.select('td[data-title*="Heute"]')[0].get_text(strip=True) if item.select('td[data-title*="Heute"]') else None
      if value and value not in [None, 'None', 'kein Pollenflug']:
        if 'starker' in value:
          value = '+++'
        elif 'ß' in value:
          value = '++'
        elif value == 'schwacher Pollenflug':
          value = '+'
        elif 'kein bis schwacher Pollenflug' in value:
          value = ''
        items.append(f"{name}{value}")
  return items

if __name__ == "__main__":
  print(', '.join(scrape_pollenflug()))