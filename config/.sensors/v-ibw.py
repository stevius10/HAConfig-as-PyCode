import requests
import json
from bs4 import BeautifulSoup

def scrape_ibw():
  items = []
  request_url = 'https://inberlinwohnen.de/wp-content/themes/ibw/skript/wohnungsfinder.php'
  request_headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': '*/*',
    'X-Requested-With': 'XMLHttpRequest'
  }
  request_data = {
    'q': 'wf-save-srch',
    'save': 'false',
    'qm_min': '50',
    'miete_max': '600',
    'rooms_min': '2',
    'bez[]': ['01_00', '02_00', '03_00', '04_00', '02_00'],
    'wbs': 0
  }
  response = requests.post(request_url, headers=request_headers, data=request_data, verify=False).text
  content = BeautifulSoup(json.loads(response)['searchresults'], 'html.parser')
  items_website = content.find_all(class_='_tb_left')
  for item in items_website:
    item_text = item.get_text().replace(' ', ' ')
    detail, address = item_text.split('|')
    items.append(f"{address} ({detail})")
  return items

if __name__ == "__main__":
  print(', '.join(scrape_ibw())[:254])