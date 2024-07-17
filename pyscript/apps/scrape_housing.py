import json
import random
import regex as re
import requests
from bs4 import BeautifulSoup

from constants.config import CFG_SERVICE_ENABLED_SCRAPE_HOUSING
from constants.data import DATA_SCRAPE_HOUSING_PROVIDERS
from constants.expressions import EXPR_TIME_SCRAPE_HOUSINGS_UPDATE, EXPR_TIME_GENERAL_WORKTIME
from constants.mappings import MAP_EVENT_SYSTEM_STARTED, MAP_PERSISTENCE_PREFIX_SCRAPE_HOUSING
from constants.settings import SET_SCRAPE_HOUSING_BLACKLIST, SET_SCRAPE_HOUSING_DELAY_RANDOM_MIN, \
  SET_SCRAPE_HOUSING_DELAY_RANDOM_MAX, SET_SCRAPE_HOUSING_FILTER_RENT

from utils import *

trigger = []

housing_provider = DATA_SCRAPE_HOUSING_PROVIDERS

# Factory
def scrape_housing_factory(provider):
  
  @event_trigger(MAP_EVENT_SYSTEM_STARTED)
  @time_trigger('shutdown')
  def scrape_housing_init():
    if service.has_service("pyscript", "store"):
      service.call(domain="pyscript", name="store", entity=get_entity(provider), default="none")

  @logged
  @service(f"pyscript.scrape_housing_{provider}", supports_response="optional")
  def scrape_housing(provider=provider):
    try:
      structure = housing_provider[provider]["structure"]
      apartments = scrape(fetch(provider),
        structure["item"], structure["address_selector"], structure["rent_selector"],
        structure["size_selector"], structure["rooms_selector"], structure["details_selector"]) or {}
      if service.has_service("pyscript", "store"):
        service.call(domain="pyscript", name="store", entity=get_entity(provider), value=apartments[:254], attributes={'url': housing_provider.get(provider).get('url')})
      return { get_entity(provider): { "value": apartments[:254], "url": housing_provider.get(provider).get('url') } } if apartments else {}
    except Exception as e:
      return { get_entity(provider): { "error": str(e), "url": housing_provider.get(provider).get('url') } } if apartments else {}
      
  trigger.append(scrape_housing)

# Automation
@time_trigger(EXPR_TIME_SCRAPE_HOUSINGS_UPDATE)
@time_trigger(EXPR_TIME_GENERAL_WORKTIME)
def scrape_housings():
  if CFG_SERVICE_ENABLED_SCRAPE_HOUSING:
    for provider in housing_provider.keys():
      task.unique(f"scrape_housing_{provider}")
      task.executor(scrape_housing_factory(provider))

def scrape(content, item_selector, address_selector, rent_selector, size_selector, rooms_selector, details_selector):
  elements = content.select(item_selector)
  apartments = []

  for element in elements:
    element_text = element.get_text(" ", strip=True)
    
    address = get_or_default(element, address_selector)
    if not address:
      address_match = re.search(r'([^,\d]+)\s*(\d{5})?\s*(Berlin)?', element_text)
      address = address_match.group() if address_match else None

    if not address:
      continue

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

    apartment = filtering({"address": address, "rent": rent, "size": size, "rooms": rooms, "details": details, "text": element_text})
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

# Helper
def get_entity(provider):
  return f"pyscript.{MAP_PERSISTENCE_PREFIX_SCRAPE_HOUSING}_{provider}"

def get_or_default(element, selector, default=None):
  if not selector:
    return default
  if isinstance(selector, str):
    item = element.select_one(selector)
    if item:
      text = item.get_text().strip()
      return text if text else default
    else:
      return default
  elif callable(selector):
    return selector(element)
  return default

def get_or_default_format(text):
  text.replace("\\n", ", ")
  text.replace(" | ", ", ")
  return text

# Initialization
for provider in housing_provider.keys():
  scrape_housing_factory(provider)
