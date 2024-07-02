from constants.config import *
from constants.mappings import *
from constants.settings import *

from utils import *

# Automation

# Housing

@state_trigger(expr(entity=[name for name in state.names() if PERSISTANCE_SCRAPE_HOUSING_SENSOR_PREFIX in name]))
@logged
def notify_housing(target=DEFAULT_NOTIFICATION_TARGET, default=True, var_name=None, value=None, old_value=None):
  if value and value not in STATES_UNDEFINED:
    url = SERVICE_SCRAPE_HOUSING_PROVIDERS.get(var_name.split(f"{PERSISTANCE_SCRAPE_HOUSING_SENSOR_PREFIX}_")[1]).get("url")
    pyscript.shortcut(message=f"{var_name}: {value}", shortcut=SHORTCUT_HOUSING_NAME, input=url)