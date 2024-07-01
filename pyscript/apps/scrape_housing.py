from constants.config import SERVICE_SCRAPE_HOUSING_ENABLED
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
  if apartment.get("address") is None:
    return None
  if apartment.get("rent") is not None:
    if re.findall(r'\d', apartment["rent"]) and not (400 < int(''.join(re.findall(r'\d', apartment["rent"])[:3])) < SERVICE_SCRAPE_HOUSING_FILTER_RENT):
      return None
  if apartment.get("details") is not None:
    for blacklist_item in SERVICE_SCRAPE_HOUSING_BLACKLIST_DETAILS:
      if re.search(r'\b' + re.escape(blacklist_item.lower()) + r'\b', apartment["details"].lower()):
        return None
  return {k: v for k, v in apartment.items() if v is not None}

def scrape(content, item, address_selector, rent_selector, size_selector=None, rooms_selector=None, details_selector=None):
  apartments = []
  elements = content.select(item)
  
  for element in elements:
    element_text = element.get_text(strip=True)
    
    address = get_or_default(element, address_selector)
    if not address:
      address_match = re.search(r'([A-Za-zäöüß\s.-]+\s\d+(?:,\s*[A-Za-zäöüß\s-]+)?)', element_text)
      address = address_match.group(1) if address_match else None
    
    rent = get_or_default(element, rent_selector)
    if not rent:
      rent_match = re.search(r'(\d+(?:,\d+)?)\s*€', element_text)
      rent = rent_match.group(1) + ' €' if rent_match else None
    
    size = get_or_default(element, size_selector)
    if not size:
      size_match = re.search(r'(\d+(?:,\d+)?)\s*m²', element_text)
      size = size_match.group(1) + ' m²' if size_match else None
    
    rooms = get_or_default(element, rooms_selector)
    if not rooms:
      rooms_match = re.search(r'(\d+(?:,\d+)?)\s*Zimmer', element_text)
      rooms = rooms_match.group(1) + ' Zimmer' if rooms_match else None
    
    details = get_or_default(element, details_selector)
    if not details:
      details = element_text
    
    apartment = filter({"address": address, "rent": rent, "size": size, "rooms": rooms, "details": details})
    if apartment:
      summary = [item for item in [rent, rooms, size] if item]
      apartment_format = f"{address} ({', '.join(summary)})" if summary else address
      apartments.append(apartment_format)
  
  apartments_format = ", ".join(apartments)
  return apartments_format

@pyscript_executor
def fetch(provider):
  if housing_provider[provider].get("request_headers") and housing_provider[provider].get("request_data"):
    response = requests.post(housing_provider[provider]["url"], headers=housing_provider[provider]["request_headers"], data=housing_provider[provider]["request_data"], verify=False).text
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
    state.persist(get_entity(provider), default_value="")

  @time_trigger(EXPR_TIME_UPDATE_SENSORS_HOUSING)
  @state_active(str(SERVICE_SCRAPE_HOUSING_ENABLED))
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
      return f"{provider}: {str(apartments)}"
    debug(f"{provider}: [{housing_provider.get(provider).get('url')}")

  trigger.append(scrape_housing)

# Initialization

@logged
@service
def scrape_housings(housing_provider=housing_provider):
  for provider in housing_provider.keys():
    pyscript.scrape_housing(provider=provider, blocking=False, return_response=False)
  return

for provider in housing_provider.keys():
  scrape_housing_factory(provider)

# Helper

def get_entity(provider):
  return f"pyscript.{PERSISTANCE_SCRAPE_HOUSING_SENSOR_PREFIX}_{provider}"

def get_or_default(element, selector, default=None):
  if not selector:
    return default
  if isinstance(selector, str):
    item = element.select_one(selector)
    return item.get_text().strip() if item else default
  elif callable(selector):
    return selector(element)
  return default