from constants.events import *
from constants.expressions import *
from constants.mappings import *
from constants.settings import *

from utils import *

import json
import random
import requests
from bs4 import BeautifulSoup

trigger = []

housing_provider = SERVICE_SCRAPE_HOUSING_PROVIDERS

# Function

@logged
def scrape(content, item, address_selector, area_selector, rent_selector, size_selector=None, rooms_selector=None, details_selector=None):
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
  
# Factory

def scrape_housing_factory(provider):

  entity = f"pyscript.{PERSISTANCE_SCRAPE_HOUSING_SENSOR_PREFIX}_{provider}"
  
  @time_trigger('startup')
  @time_trigger('shutdown')
  def scrape_housing_init():
    state.persist(entity, default_value="none")

  @time_trigger(EXPR_TIME_UPDATE_SENSORS_HOUSING)
  @time_active(EXPR_TIME_GENERAL_WORKTIME)
  @logged
  @service
  def scrape_housing(provider=provider):
    task.sleep(random.randint(SERVICE_SCRAPE_HOUSING_DELAY_RANDOM_MIN, SERVICE_SCRAPE_HOUSING_DELAY_RANDOM_MAX))
    
    structure = housing_provider[provider]["structure"]
    if housing_provider[provider].get("request_headers") and housing_provider[provider].get("request_data"):
      response = requests.post(housing_provider[provider]["url"], headers=housing_provider[provider].get("request_headers"), data=housing_provider[provider].get("request_data"), verify=False).text
      content = BeautifulSoup(json.loads(response)['searchresults'], 'html.parser')
    else: 
        response = requests.get(housing_provider[provider]["url"], verify=verify)
        content = BeautifulSoup(response.content, 'html.parser')

    state.set(entity, scrape(content, structure["item"], 
      structure["address_selector"], structure["area_selector"], structure["rent_selector"], 
      structure["size_selector"], structure["rooms_selector"], structure["details_selector"] ))
    log(f"{entity} set to {state.get(entity)}", kwargs.get("context"))
    log_data(state.getattr(entity))
    
  trigger.append(scrape_housing)

# Initialization

for provider in housing_provider.keys():
  scrape_housing_factory(provider)

event.fire(EVENT_HOUSING_INITIALIZED)