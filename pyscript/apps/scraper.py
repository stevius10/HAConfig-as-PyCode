from constants.expressions import *
from constants.settings import *

from utils import *

import json
import requests
from bs4 import BeautifulSoup

def fetch(url, method="GET", headers=None, data=None, verify=False):
  response = requests.request(method, url, headers=headers, data=data, verify=verify)
  return BeautifulSoup(response.content, 'html.parser')

def extract(content, item, address_selector, area_selector, rent_selector, size_selector=None, rooms_selector=None, details_selector=None):
  apartments = []
  
  elements = content.select(item)
  for element in elements:
    address = element.select_one(address_selector).get_text().strip() if element.select_one(address_selector) else None
    area = element.select_one(area_selector).get_text().strip() if element.select_one(area_selector) else None
    rent = element.select_one(rent_selector).get_text().strip() if element.select_one(rent_selector) else None
    size = element.select_one(size_selector).get_text().strip() if size_selector and element.select_one(size_selector) else None
    rooms = element.select_one(rooms_selector).get_text().strip() if rooms_selector and element.select_one(rooms_selector) else None
    details = element.select_one(details_selector).get_text() if details_selector and element.select_one(details_selector) else None

    apartments.append({"address": address, "area": area, "rent": rent, "size": size, "rooms": rooms, "details": details })

  return apartments

def set_sensor(provider, apartments):
  state.set(f"{SERVICE_SCRAPE_HOUSING_SENSOR_PREFIX}_{provider}", ', '.join(apartments[SERVICE_SCRAPE_HOUSING_SENSOR_LENGTH]))
  
def scrape_housing_factory(provider):

  @time_trigger(EXPR_TIME_UPDATE_SENSORS_HOUSING)
  @time_active(EXPR_TIME_GENERAL_WORKTIME)
  @logged
  @service
  def scrape_housing(provider):
    task.sleep(random.randint(SERVICE_SCRAPE_HOUSING_DELAY_RANDOM_MIN, SERVICE_SCRAPE_HOUSING_DELAY_RANDOM_MAX))
      
    url = SERVICE_SCRAPE_HOUSING_PROVIDERS[provider]["url"]
    if SERVICE_SCRAPE_HOUSING_PROVIDERS[provider].get("request_headers") and SERVICE_SCRAPE_HOUSING_PROVIDERS[provider].get("request_data"):
      response = requests.post(url, headers=HOUSING_PROVIDERS[provider].get("request_headers"), data=HOUSING_PROVIDERS[provider].get("request_data"), verify=False).text
      content = BeautifulSoup(json.loads(response)['searchresults'], 'html.parser')
    else: 
      content = fetch(url)
    
    structure = SERVICE_SCRAPE_HOUSING_PROVIDERS[provider]["structure"]
    item = structure["item"]
    address_selector = structure["address_selector"]
    area_selector = structure["area_selector"]
    rent_selector = structure["rent_selector"]
    size_selector = structure["size_selector"]
    rooms_selector = structure["rooms_selector"]
    details_selector = structure["details_selector"]
  
    set_sensor(provider, extract(
      content, item, address_selector, area_selector, rent_selector, size_selector, rooms_selector, details_selector 
    ))

for provider in SERVICE_SCRAPE_HOUSING_PROVIDERS.keys():
  state.persist(f"pyscript.{provider}")
  apartments = scrape_housing_factory(provider)
  
