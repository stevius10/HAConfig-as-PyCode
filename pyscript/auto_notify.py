from constants.config import DEFAULT_NOTIFICATION_TARGET
from constants.data import DATA_SCRAPE_HOUSING_PROVIDERS
from constants.mappings import PERSISTENCE_PREFIX_SENSOR_SCRAPE_HOUSING, MAP_SERVICE_SCRAPE_HOUSING_SHORTCUT_NAME

from utils import *

def get_identifiers(text):
  identifiers, current = [], ''
  for char in text:
    if char == '(':
      identifiers.append(''.join(c.lower() for c in current if c.isalnum()))
      current = ''
    elif char != ')':
      current += char
  if current:
    identifiers.append(''.join(c.lower() for c in current if c.isalnum()))
  return identifiers

def compare(old, new):
  old_identifiers = set(get_identifiers(old))
  new_identifiers = set(get_identifiers(new))
  return new_identifiers - old_identifiers

@state_trigger(expr(entity=[name for name in state.names() if PERSISTENCE_PREFIX_SENSOR_SCRAPE_HOUSING in name]))
@logged
def notify_housing(target=DEFAULT_NOTIFICATION_TARGET, default=True, var_name=None, value=None, old_value=None):
  if value and value not in MAP_STATE_HA_UNDEFINED:
    diff = compare(old_value, value)
  if diff:
    url = DATA_SCRAPE_HOUSING_PROVIDERS.get(var_name.split(f"{PERSISTENCE_PREFIX_SENSOR_SCRAPE_HOUSING}_")[1]).get("url")
    pyscript.shortcut(message=f"{var_name}: {', '.join(diff)}", shortcut=MAP_SERVICE_SCRAPE_HOUSING_SHORTCUT_NAME, input=url)
    url = DATA_SCRAPE_HOUSING_PROVIDERS.get(var_name.split(f"{PERSISTENCE_PREFIX_SENSOR_SCRAPE_HOUSING}_")[1]).get("url")
    pyscript.shortcut(message=f"{var_name}: {value}", shortcut=MAP_SERVICE_SCRAPE_HOUSING_SHORTCUT_NAME, input=url)