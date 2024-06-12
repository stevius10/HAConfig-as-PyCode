from constants.config import *
from constants.devices import *
from constants.expressions import *
from constants.mappings import *
from constants.settings import *

from utils import *

import random

# Automation

# Housing
@state_trigger(expr([f"{SERVICE_SCRAPE_HOUSING_SENSOR_PREFIX}_{key}" for key in SERVICE_SCRAPE_HOUSING_PROVIDERS.keys()]))
def notify_housing(target=DEFAULT_NOTIFICATION_TARGET, default=True, var_name=None, value=None, old_value=None):
  if value not in STATES_UNDEFINED:
    pyscript.shortcut(message=f"{var_name}: {value}", shortcut=SHORTCUT_HOUSING_NAME, input=sensors.get(var_name).get(SHORTCUT_HOUSING_PARAMETER_URL))