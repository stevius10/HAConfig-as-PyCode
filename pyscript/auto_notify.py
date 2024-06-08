from constants.config import *
from constants.devices import *
from constants.entities import *
from constants.expressions import *
from constants.mappings import *
from constants.settings import *

from utils import expr

import random

sensors = AUTO_NOTIFY_SENSORS_HOUSING
default_notification_target = DEFAULT_NOTIFICATION_TARGET

# Automation

@state_trigger(expr([str(key) for key in sensors.keys()]))
def notify_housing(target=default_notification_target, default=True, var_name=None, value=None, old_value=None):
  pyscript.shortcut(message=f"{var_name}: {value}", shortcut=SHORTCUT_HOUSING_NAME, input=sensors.get(var_name).get(SHORTCUT_HOUSING_PARAMETER_URL))

# Helper

@time_trigger(EXPR_TIME_UPDATE_SENSORS_HOUSING)
@time_active(EXPR_TIME_GENERAL_WORKTIME)
def update_sensors_housing(sensors=sensors):
  task.sleep(random.randint(AUTO_NOTIFY_SCRAPE_HOUSING_DELAY_RANDOM_MIN, AUTO_NOTIFY_SCRAPE_HOUSING_DELAY_RANDOM_MAX))
  for sensor in sensors:
    homeassistant.update_entity(entity_id=sensor)