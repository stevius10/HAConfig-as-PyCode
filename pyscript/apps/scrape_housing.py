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
    
  provider = provider

  @event_trigger(MAP_EVENT_SYSTEM_STARTED)
  @time_trigger('shutdown')
  def scrape_housing_persistence():
    if service.has_service("pyscript", "persistence"):
      service.call(domain="pyscript", name="persistence", entity=get_entity(provider))

  @debugged
  @service(f"pyscript.scrape_housing_{provider}", supports_response="optional")
  def scrape_housing():
    structure = housing_provider[provider]["structure"]
    try:
      apartments = scrape(fetch(provider), 
        structure["item"], structure["address_selector"], structure["rent_selector"],
        structure["size_selector"], structure["rooms_selector"], structure["details_selector"])
      apartments_result = apartments[:254] if apartments else ""
      
      attributes = {'url': housing_provider.get(provider, {}).get('url', '')}
      store(entity=get_entity(provider), value=apartments_result, attributes=attributes)
        
      return { "provider": provider, "result": apartments_result, "details": attributes } 
    
    except Exception as e:
      raise Exception(f"{type(e).name}: {str(e)}")

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
    if len(result_housing.get('result', '0')) > 0: results_housing.append(result_housing)

  return results_housing

# Functional

@pyscript_executor
def fetch(provider):
  try: 
    if housing_provider[provider].get("request_headers") and housing_provider[provider].get("request_data"):
      response = requests.post(housing_provider[provider]["url"], headers=housing_provider[provider]["request_headers"], data=housing_provider[provider]["request_data"], verify=False).text
      content = BeautifulSoup(json.loads(response)['searchresults'], 'html.parser')
    else:
      response = requests.get(housing_provider[provider]["url"], verify=False)
      content = BeautifulSoup(response.content, 'html.parser')
    return content
  except Exception as e:
    raise Exception(f"{type(e).name}: {str(e)}")

@pyscript_executor
def scrape(content, item, address_selector, rent_selector, size_selector=None, rooms_selector=None, details_selector=None):
  apartments = []
  elements = content.select(item)
  
  for element in elements:
    try:
      element_text = element.get_text(strip=True)
      address = get_or_default(element, address_selector) or find(element_text, r'([A-Za-zäöüß\s.-]+\s\d+(?:,\s*\d{5})?)')
      rent = get_or_default(element, rent_selector) or find(element_text, r'(\d+(?:,\d+)?)\s*€')
      size = get_or_default(element, size_selector) or find(element_text, r'(\d+(?:,\d+)?)\s*(m²|m2|qm|Quadratmeter)')
      rooms = get_or_default(element, rooms_selector) or find(element_text, r'(\d+(?:,\d+)?)\s*Zimmer')
      details = get_or_default(element, details_selector) or element_text
    
      apartment = filtering(element, {"address": address, "rent": rent, "size": size, "rooms": rooms, "details": details, "text": element_text})
      if apartment:
        summary = [item for item in [rent, rooms, size] if item]
        apartments.append(f"{address} ({', '.join(summary)})" if summary else address)
    except Exception as e:
      continue
  
  return ", ".join(apartments)
 
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