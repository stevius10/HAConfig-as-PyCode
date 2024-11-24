import json
import random
import regex as re
import requests
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict
from bs4 import BeautifulSoup

from constants.config import CFG_PATH_DIR_PY_LOGS_DATA, CFG_SERVICE_ENABLED_SCRAPE_HOUSING
from constants.data import DATA_SCRAPE_HOUSING_PROVIDERS
from constants.expressions import EXPR_TIME_SCRAPE_HOUSINGS_UPDATE, EXPR_TIME_GENERAL_WORKTIME
from constants.mappings import MAP_EVENT_SYSTEM_STARTED, MAP_PERSISTENCE_PREFIX_SCRAPE_HOUSING, MAP_RESULT_STATUS
from constants.settings import *

from utils import *

trigger = []

housing_provider = DATA_SCRAPE_HOUSING_PROVIDERS

# Factory 

def scrape_housing_factory(provider):
  @event_trigger(MAP_EVENT_SYSTEM_STARTED)
  @time_trigger('shutdown')
  def scrape_housing_persistence():
    store(entity=get_entity(provider))

  @service(f"pyscript.scrape_housing_{provider}", supports_response="optional")
  @debugged
  def scrape_housing(provider=provider):
    try:
      structure = housing_provider[provider]["structure"]
      apartments, ignore = scrape(fetch(provider), 
        structure["item"], structure["address_selector"], structure["rent_selector"],
        structure["size_selector"], structure["rooms_selector"], structure["details_selector"])
      
      formated = format_apartments([format_apartment(apartment) for apartment in apartments])
      store(entity=get_entity(provider), value=formated)

      return { "entity": get_entity(provider), MAP_RESULT_STATUS.ITEMS: apartments, MAP_RESULT_STATUS.IGNORE: ignore }
    except Exception as e:
      return { "entity": get_entity(provider), MAP_RESULT_STATUS.ERROR: str(e) }

  trigger.append([scrape_housing_persistence, scrape_housing])

# Main

@time_trigger(EXPR_TIME_SCRAPE_HOUSINGS_UPDATE)
@state_active(str(CFG_SERVICE_ENABLED_SCRAPE_HOUSING))
@time_active(EXPR_TIME_GENERAL_WORKTIME)
@logged
@service
def scrape_housings(housing_provider=housing_provider, event_trigger=None):
  logfile = get_logfile(f"{pyscript.get_global_ctx()}_{datetime.now().strftime('%d-%m-%y')}", log_dir=CFG_PATH_DIR_PY_LOGS_DATA)

  if event_trigger: 
    task.sleep(random.randint(SET_SCRAPE_HOUSING_DELAY_RANDOM_MIN, SET_SCRAPE_HOUSING_DELAY_RANDOM_MAX))

  results = {"items": [], "ignore": []}

  for provider in housing_provider.keys():
    result = service.call("pyscript", f"scrape_housing_{provider}", return_response=True)

    if result[MAP_RESULT_STATUS.ITEMS]:
      logfile.log(str(result[MAP_RESULT_STATUS.ITEMS]))
      results['items'].append(result[MAP_RESULT_STATUS.ITEMS])
    if result[MAP_RESULT_STATUS.IGNORE]:
      results['ignore'].append(result[MAP_RESULT_STATUS.IGNORE])

  return results

# Logic

def scrape(content, item, address_selector, rent_selector, size_selector=None, rooms_selector=None, details_selector=None) -> List[Apartment]:
  apartments = []
  discarded = []
  elements = content.select(item)
  
  for element in elements:
    element_text = element.get_text(strip=True)
    
    # Scrape
    
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

    plz = re.search(r'\b1\d{4}\b', address)

    apartment = {"address": address, "rent": rent, "size": size, "rooms": rooms, "details": details, "text": element_text}
    
    # Filtering
    
    if [apartment.get('rent'), apartment.get('size'), apartment.get('rooms'), apartment.get('details')].count(None) == 4 or apartment.get('address') is None or \
    (apartment.get('rent') is not None and re.findall(r'\d', apartment.get('rent')) and not (400 < int(''.join(re.findall(r'\d', apartment.get('rent'))[:3])) < SET_SCRAPE_HOUSING_FILTER_RENT)) or \
    (plz and hasattr(plz, 'group') and plz.group().startswith('1') and plz.group() not in ['12043', '12045', '12047', '12049', '12051', '12053', '13573', '12089']) or \
    (apartment.get('text') is not None and True in [re.search(r'\b' + re.escape(item.lower()) + r'\b', apartment.get('text').lower()) for item in SET_SCRAPE_HOUSING_BLACKLIST]):
      discarded.append(apartment)
    else:
      apartments.append(apartment)

  return apartments, discarded

@pyscript_executor
def fetch(provider):
  if housing_provider[provider].get("request_headers") and housing_provider[provider].get("request_data"):
    response = requests.post(housing_provider[provider]["url"], headers=housing_provider[provider]["request_headers"], data=housing_provider[provider]["request_data"], verify=False).text
    content = BeautifulSoup(json.loads(response)['searchresults'], 'html.parser')
  else:
    response = requests.get(housing_provider[provider]["url"], verify=False)
    content = BeautifulSoup(response.content, 'html.parser')
  return content

# Utility 

def format_apartment(apartment):
  return f"{apartment.get('address', '')} ({apartment.get('rent', '')}{', ' if apartment.get('rent') and apartment.get('rooms') else ''}{apartment.get('rooms', '')}{', ' if (apartment.get('rent') or apartment.get('rooms')) and apartment.get('size') else ''}{apartment.get('size', '')})"[:254].strip(" ()")

def format_apartments(apartments):
  return ", ".join([apartment for apartment in apartments])[:254]

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