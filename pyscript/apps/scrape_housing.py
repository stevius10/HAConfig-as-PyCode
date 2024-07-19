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
  
  # pyscript.store(entity=get_entity(provider))

  @event_trigger(MAP_EVENT_SYSTEM_STARTED)
  @time_trigger('shutdown')
  def scrape_housing_persistence():
    if service.has_service("pyscript", "store"):
      service.call(domain="pyscript", name="store", entity=get_entity(provider))

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
@state_active(str(CFG_SERVICE_ENABLED_SCRAPE_HOUSING))
@time_active(EXPR_TIME_GENERAL_WORKTIME)
@logged
@service
def scrape_housings(housing_provider=housing_provider, event_trigger=None):
  results_housing = []
  
  if event_trigger: 
    task.sleep(random.randint(SET_SCRAPE_HOUSING_DELAY_RANDOM_MIN, SET_SCRAPE_HOUSING_DELAY_RANDOM_MAX))

  for provider in housing_provider.keys():
    result_housing = service.call("pyscript", f"scrape_housing_{provider}", return_response=True)
    if len(result_housing.get('result', '0')) > 0: 
      results_housing.append(result_housing) if result_housing else ""

  return { "result": results_housing if results_housing else {} }

# Functional

@debugged
def filtering(apartment):
  if all([value is None for value in apartment.values()]):
    return None
  if apartment.get("address") is None:
    return None
  if apartment.get("rent") is not None:
    if re.findall(r'\d', apartment["rent"]) and not (400 < int(''.join(re.findall(r'\d', apartment["rent"])[:3])) < SET_SCRAPE_HOUSING_FILTER_RENT):
      return None
  if apartment.get("text") is not None:
    for blacklist_item in SET_SCRAPE_HOUSING_BLACKLIST:
      if re.search(r'\b' + re.escape(blacklist_item.lower()) + r'\b', apartment["text"].lower()):
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
    return item.get_text().strip() if item else default
  elif callable(selector):
    return selector(element)
  return default

def get_or_default_format(text):
  text = text.replace("\n", ", ")
  text = text.replace(" | ", ", ")
  return text

# Initialization

for provider in housing_provider.keys():
  scrape_housing_factory(provider)