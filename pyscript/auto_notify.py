from constants.config import *
from constants.devices import *
from constants.events import *
from constants.expressions import *
from constants.mappings import *
from constants.settings import *

from utils import *

import random

trigger = []

# Automation

# Housing
  
def get_housing(prefix=PERSISTANCE_SCRAPE_HOUSING_SENSOR_PREFIX):
  sensors = []
  for name in state.names(domain="pyscript"):
    if prefix in name: sensors.append(name)

@event_trigger(EVENT_HOUSING_INITIALIZED)
def init_housing():
  @state_trigger(expr(get_housing()))
  def notify_housing(target=DEFAULT_NOTIFICATION_TARGET, default=True, var_name=None, value=None, old_value=None):
    if value not in STATES_UNDEFINED:
      pyscript.shortcut(message=f"{var_name}: {value}", shortcut=SHORTCUT_HOUSING_NAME, input=sensors.get(var_name).get(SHORTCUT_HOUSING_PARAMETER_URL))
  trigger.append(notify_housing)