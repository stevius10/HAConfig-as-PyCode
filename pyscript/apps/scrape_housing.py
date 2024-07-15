import json
import random
import regex as re
import requests
from bs4 import BeautifulSoup

from constants.config import CFG_SERVICE_ENABLED_SCRAPE_HOUSING
from constants.data import DATA_SCRAPE_HOUSING_PROVIDERS
from constants.expressions import EXPR_TIME_SCRAPE_HOUSINGS_UPDATE, EXPR_TIME_GENERAL_WORKTIME
from constants.mappings import MAP_EVENT_SYSTEM_STARTED, MAP_PERSISTENCE_PREFIX_SCRAPE_HOUSING
from constants.settings import SET_SCRAPE_HOUSING_BLACKLIST, SET_SCRAPE_HOUSING_DELAY_RANDOM_MIN, SET_SCRAPE_HOUSING_DELAY_RANDOM_MAX, SET_SCRAPE_HOUSING_FILTER_RENT

from utils import *

trigger = []

housing_provider = DATA_SCRAPE_HOUSING_PROVIDERS

def scrape_housing_factory(provider):
  @event_trigger(MAP_EVENT_SYSTEM_STARTED)
  @time_trigger('shutdown')
  def scrape_housing_store():
    store(entity=get_entity(provider))

  @service(f"pyscript.scrape_housing_{provider}", supports_response="optional")
  @logged
  def scrape_housing():
    structure = housing_provider[provider]["structure"]
    try:
      apartments = scrape(fetch(provider), structure)
      apartments_result = apartments[:254] if apartments else ""
      
      attributes = {'url': housing_provider.get(provider).get('url')}

      store(entity=get_entity(provider), value=apartments_result, attributes=attributes)
        
      return { "provider": provider, "result": apartments_result, "details": attributes } 
    except Exception as e:
      raise Exception(f"{type(e).name}: {str(e)}")

  trigger.append(scrape_housing)

@time_trigger(EXPR_TIME_SCRAPE_HOUSINGS_UPDATE)
@state_active(str(CFG_SERVICE_ENABLED_SCRAPE_HOUSING))
@time_active(EXPR_TIME_GENERAL_WORKTIME)
@logged
@service
def scrape_housings(housing_provider=housing_provider, event_trigger=None):
  results_housing = {}
  
  if event_trigger: 
    task.sleep(random.randint(SET_SCRAPE_HOUSING_DELAY_RANDOM_MIN, SET_SCRAPE_HOUSING_DELAY_RANDOM_MAX))

  for provider in housing_provider.keys():   
    result_housing = service.call("pyscript", f"scrape_housing_{provider}", return_response=True)
    if len(result_housing.get('result', '0')) > 0: results_housing.append({ provider: result_housing})

  return results_housing

@pyscript_executor
def fetch(provider):
  try: 
    if housing_provider[provider].get("request_headers") or housing_provider[provider].get("request_data"):
      response = requests.post(housing_provider[provider].get("url", {}), headers=housing_provider[provider].get("request_headers", {}), data=housing_provider[provider].get("request_data", {}), verify=False).text
      content = BeautifulSoup(response, 'html.parser')  # Removed JSON parsing, handle as HTML directly
    else:
      response = requests.get(housing_provider[provider]["url"], verify=False)
      content = BeautifulSoup(response.content, 'html.parser')
    return content
  except Exception as e:
    raise Exception(f"{type(e).name}: {str(e)}")

@pyscript_executor
def scrape(content, structure):
  apartments = []
  elements = content.select(structure["item"])
  
  for element in elements:
    try:
      element_text = element.get_text(strip=True)
      address = extract(element, structure.get("address_selector"), element_text, r'([A-Za-zäöüß\s.-]+\s\d+(?:,\s*\d{5})?)')
      rent = extract(element, structure.get("rent_selector"), element_text, r'(\d+(?:,\d+)?)\s*€')
      size = extract(element, structure.get("size_selector"), element_text, r'(\d+(?:,\d+)?)\s*(m²|m2|qm|Quadratmeter)')
      rooms = extract(element, structure.get("rooms_selector"), element_text, r'(\d+(?:,\d+)?)\s*Zimmer')
      details = get_or_default(element, structure.get("details_selector"), element_text)
    
      apartment = filtering({"address": address, "rent": rent, "size": size, "rooms": rooms, "details": details, "text": element_text})
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
  item = element.select_one(selector) if isinstance(selector, str) else selector(element)
  return item.get_text().strip() if item else default

def extract(element, selector, text, pattern):
  return get_or_default(element, selector) or find(text, pattern)

def find(text, pattern):
  match = re.search(pattern, text)
  return match.group(1) if match else None

# Initialization

for provider in housing_provider.keys():
  scrape_housing_factory(provider)
