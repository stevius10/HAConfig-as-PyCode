from constants.events import *
from constants.expressions import *
from constants.mappings import *
from constants.settings import *

from utils import *

import json
import random
import regex as re
import requests

from bs4 import BeautifulSoup

trigger = []

housing_provider = SERVICE_SCRAPE_HOUSING_PROVIDERS

# Function

@debugged
def filter(apartment):
  if all([value is None for value in apartment.values()]):
    return None
  if apartment["address"] is None:
    return None
  if apartment["rent"] is not None:
    if re.findall(r'\d', apartment["rent"]) and not (400 < int(''.join(re.findall(r'\d', apartment["rent"])[:3])) < SERVICE_SCRAPE_HOUSING_FILTER_RENT):
      return None
  return {k: v for k, v in apartment.items() if v is not None}

def scrape(content, item, address_selector, rent_selector, size_selector=None, rooms_selector=None, details_selector=None):
  apartments = []
  elements = content.select(item)
  
  for element in elements:
    address = get_or_default(element, address_selector)
    rent = get_or_default(element, rent_selector)
    size = get_or_default(element, size_selector)
    rooms = get_or_default(element, rooms_selector)
    details = get_or_default(element, details_selector)
    apartment = filter({ "address": address, "rent": rent, "size": size, "rooms": rooms, "details": details })
    if apartment:
      details = [detail for detail in [rent, rooms, size] if detail] 
      apartment_format = f"{address} ({', '.join(details)})" if details else address
      apartments.append(apartment_format)
      
  apartments_format = ", ".join(apartments)

  return apartments_format

@pyscript_executor
def fetch(provider):
  if housing_provider[provider].get("request_headers") and housing_provider[provider].get("request_data"):
    response = (requests.post(housing_provider[provider]["url"], headers=housing_provider[provider].get("request_headers"), data=housing_provider[provider].get("request_data"), verify=False)).text
    content = BeautifulSoup(json.loads(response)['searchresults'], 'html.parser')
  else:
    response = requests.get(housing_provider[provider]["url"], verify=False)
    content = BeautifulSoup(response.content, 'html.parser')
  return content

# Factory

def scrape_housing_factory(provider):

  @time_trigger('startup')
  @time_trigger('shutdown')
  def scrape_housing_init():
    state.persist(get_entity(provider))

  @time_trigger(EXPR_TIME_UPDATE_SENSORS_HOUSING)
  @time_active(EXPR_TIME_GENERAL_WORKTIME)
  @logged
  @service
  def scrape_housing(provider=provider):
    task.sleep(random.randint(SERVICE_SCRAPE_HOUSING_DELAY_RANDOM_MIN, SERVICE_SCRAPE_HOUSING_DELAY_RANDOM_MAX))
    
    structure = housing_provider[provider]["structure"]
    apartments = scrape(fetch(provider), 
      structure["item"], structure["address_selector"], structure["rent_selector"],
      structure["size_selector"], structure["rooms_selector"], structure["details_selector"])
    
    state.set(get_entity(provider), apartments[:254])
    state.persist(get_entity(provider))
    
    if apartments: 
      apartments_result = f"{provider}: {str(apartments)}"
      debug(f"{apartments_result} \n[{housing_provider.get(provider).get('url')}")
      return apartments_result

  trigger.append(scrape_housing)

# Initialization

@logged
@service
def scrape_housings(housing_provider=housing_provider):
  for provider in housing_provider.keys():
    pyscript.scrape_housing(provider=provider, blocking=False, return_response=False)
  return

def init(): 
  for provider in housing_provider.keys():
    scrape_housing_factory(provider)

  event.fire(EVENT_HOUSING_INITIALIZED)

init()

# Helper

def get_entity(provider):
    return f"pyscript.{PERSISTANCE_SCRAPE_HOUSING_SENSOR_PREFIX}_{provider}"

def get_or_default(element, selector, default=None):
  item = element.select_one(selector) if selector and element else ""
  return item.get_text().strip() if item else default