from constants.config import *
from constants.entities import *
from constants.expressions import *
from constants.mappings import *
from constants.settings import *

from utils import *

entities = SERVICE_AIR_CLEANER_ENTITIES

@state_trigger(expr([entity["sensor"] for entity in entities.values()], SERVICE_AIR_CLEANER_THRESHOLD_START, comparator=">"))
@state_active(f"{SERVICE_AIR_MANAGEMENT_ENABLED} and {EXPR_STATE_AIR_AUTOMATION_SEASON} and {expr([entity['fan'] for entity in entities.values()], STATE_OFF)}")
@time_active(EXPR_TIME_AIR_AUTOMATION)
@debugged
def service_air_cleaner_threshold_on(var_name=None):
  service_air_cleaner_turn_off(entities.get(var_name.split(".")[1]).get("fan"))
  fan.turn_on(entity_id=entity)
  task.sleep(SERVICE_AIR_CLEANER_WAIT_ACTIVE_DELAY)
  service_air_cleaner_sleep(entity=var_name)

@state_trigger(expr([entity["sensor"] for entity in entities.values()], SERVICE_AIR_CLEANER_THRESHOLD_STOP, comparator="<"))
@state_active(f"{SERVICE_AIR_MANAGEMENT_ENABLED} and {EXPR_STATE_AIR_AUTOMATION_SEASON} and {expr([entity['fan'] for entity in entities.values()], STATE_ON)}")
@time_active(EXPR_TIME_AIR_AUTOMATION)
@debugged
def service_air_cleaner_threshold_off(var_name=None):
  service_air_cleaner_turn_off(entities.get(var_name.split(".")[1]).get("fan"))

@event_trigger(EVENT_NEVER) # required for service
@debugged
@service
def service_air_cleaner_clean(conditioned=False, entity=[entity["fan"] for entity in entities.values()]):
  fan.turn_on(entity_id=entity)
  task.sleep(SERVICE_AIR_CLEANER_WAIT_ACTIVE_DELAY)
  for item in entity: 
    percentage=service_air_cleaner_get_clean_percentage(item.split(".")[1]) if conditioned else 100
    fan.set_percentage(entity_id=item, percentage=percentage)
    service_air_cleaner_helper_air(entity=item, check=True)

@state_trigger(expr([entity["fan"] for entity in entities.values()], STATE_ON)) # reset
@state_trigger(expr([f"'{entity['fan']}.percentage'" for entity in entities.values()], \
  SERVICE_AIR_CLEANER_SLEEP_MODE_PERCENTAGE, comparator='>').replace("'", ""), # prevent interpretation \
  state_hold=SERVICE_AIR_CLEANER_TIMEOUT_CLEAN, state_check_now=True)
@debugged
@service
def service_air_cleaner_sleep(entity=[entity["fan"] for entity in entities.values()], var_name=None, state_check_now=True):
  if var_name: 
    entity = ".".join(var_name.split(".")[:2]) # handle percentage trigger
  if entity and isinstance(entity, str): 
    if state.get(entity) and state.get(entity) == STATE_ON:
      feature = str(state.get(f"{entity}.supported_features"))
      if feature in ["9", 9]: 
        fan.set_preset_mode(entity_id=entity, preset_mode=SERVICE_AIR_CLEANER_PRESET_MODE_SLEEP)
      if feature in ["1", 1]:
        fan.set_percentage(entity_id=entity, percentage=SERVICE_AIR_CLEANER_SLEEP_MODE_PERCENTAGE)
      service_air_cleaner_turn_off(entities[entity.split(".")[1]]["luftung"])
  elif isinstance(entity, list):
    fan.turn_on(entity_id=entity)
    task.sleep(SERVICE_AIR_CLEANER_WAIT_ACTIVE_DELAY)
    for item in entity: 
      service_air_cleaner_sleep(entity=item, var_name=item)

@debugged
def service_air_cleaner_turn_off(entity=[entity["fan"] for entity in entities.values()]):
  if isinstance(entity, list):
    for item in entity:
      service_air_cleaner_turn_off(item)
  else:
    pySERVICE.SERVICE_off_air(entity=entity)

def service_air_cleaner_get_clean_percentage(name):
  return min(max(SERVICE_AIR_CLEANER_CLEAN_MODE_PERCENTAGE, (int(state.get(entities[name].get("sensor"))) * 10)), 100)

@debugged
@service
def service_air_cleaner_helper_air(entity=[entity["fan"] for entity in entities.values()], helper=[entity["luftung"] for entity in entities.values()], check=False):
  if (check == False) or (sum([int(state.get(entities[item.split(".")[1]]["sensor"])) for item in entity if state.get(entities[item.split(".")[1]]["sensor"]) is not None]) > service_aIR_CLEANER_HELPER_PM_MINIMUM):
    homeassistant.turn_on(entity_id=helper)