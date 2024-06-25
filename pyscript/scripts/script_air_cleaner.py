from constants.entities import *
from constants.events import *
from constants.expressions import *
from constants.mappings import *
from constants.settings import *

from utils import *

entities = SCRIPT_AIR_CLEANER_ENTITIES

@state_trigger(expr([entity["sensor"] for entity in entities.values()], SCRIPT_AIR_CLEANER_THRESHOLD_START, comparator=">"))
@state_active(expr([entity['fan'] for entity in entities.values()], STATE_OFF))
@time_active(EXPR_STATE_AIR_THRESHOLD_SEASON and EXPR_STATE_AIR_THRESHOLD_TIME)
@task_unique("script_air_cleaner_threshold_on", kill_me=True)
@logged
def script_air_cleaner_threshold_on(var_name=None, value=None):
  entity = entities[var_name.split(".")[1]]["fan"]
  script_air_cleaner_sleep(entity) 
  task.sleep(SCRIPT_AIR_CLEANER_THRESHOLD_RETRIGGER_DELAY)

@state_trigger(expr([entity["sensor"] for entity in entities.values()], SCRIPT_AIR_CLEANER_THRESHOLD_STOP, comparator="<"))
@state_active(expr([entity['fan'] for entity in entities.values()], STATE_ON))
@time_active(EXPR_STATE_AIR_THRESHOLD_SEASON and EXPR_STATE_AIR_THRESHOLD_TIME)
@task_unique("script_air_cleaner_threshold_off", kill_me=True) 
@logged
def script_air_cleaner_threshold_off(var_name=None, value=None, ns=None, ctx=None, **kwargs):
  entity = entities[var_name.split(".")[1]]["fan"]
  script_air_cleaner_turn_off(entity)
  task.sleep(SCRIPT_AIR_CLEANER_THRESHOLD_RETRIGGER_DELAY)

@event_trigger(EVENT_NEVER) # required for service
@task_unique("-".join([entity["fan"] for entity in entities.values()]), kill_me=False)
@service
@logged
def script_air_cleaner_clean(conditioned=False, entity=[entity["fan"] for entity in entities.values()]):
  fan.turn_on(entity_id=entity)
  task.sleep(SCRIPT_AIR_CLEANER_WAIT_ACTIVE_DELAY)
  for item in entity: 
    percentage=script_air_cleaner_get_clean_percentage(item.split(".")[1]) if conditioned else 100
    fan.set_percentage(entity_id=item, percentage=percentage)
    script_air_cleaner_helper_air(entity=item)

@state_trigger(expr([entity["fan"] for entity in entities.values()], STATE_ON)) # reset
@state_trigger(expr([f"'{entity['fan']}.percentage'" for entity in entities.values()], \
  SCRIPT_AIR_CLEANER_SLEEP_MODE_PERCENTAGE, comparator='>').replace("'", ""), # prevent interpretation \
  state_hold=SCRIPT_AIR_CLEANER_TIMEOUT_CLEAN, state_check_now=True)
@debugged
@service
def script_air_cleaner_sleep(entity=[entity["fan"] for entity in entities.values()], var_name=None, state_check_now=True):
  if var_name: 
    entity = ".".join(var_name.split(".")[:2]) # handle percentage trigger
    if state.get(entity) and state.get(entity) == STATE_ON:
      feature = str(state.get(f"{entity}.supported_features"))
      if feature in ["9", 9]: 
        fan.set_preset_mode(entity_id=entity, preset_mode=SCRIPT_AIR_CLEANER_PRESET_MODE_SLEEP)
      if feature in ["1", 1]:
        fan.set_percentage(entity_id=entity, percentage=SCRIPT_AIR_CLEANER_SLEEP_MODE_PERCENTAGE)
      script_air_cleaner_turn_off(entities[entity.split(".")[1]]["luftung"])
  elif isinstance(entity, list):
    fan.turn_on(entity_id=entity)
    task.sleep(SCRIPT_AIR_CLEANER_WAIT_ACTIVE_DELAY)
    for item in entity: 
      script_air_cleaner_sleep(entity=item, var_name=item)

def script_air_cleaner_turn_off(entity=[entity["fan"] for entity in entities.values()]):
  if isinstance(entity, list):
    for item in entity:
      script_air_cleaner_turn_off(item)
  else:
    pyscript.script_off_air(entity=entity)

def script_air_cleaner_get_clean_percentage(name):
  return min(max(SCRIPT_AIR_CLEANER_CLEAN_MODE_PERCENTAGE, (int(state.get(entities[name].get("sensor"))) * 10)), 100)

@debugged
def script_air_cleaner_helper_air(entity=[entity["fan"] for entity in entities.values()], helper=[entity["luftung"] for entity in entities.values()], check=True):
  if (check == False) or (sum([int(state.get(entities[item.split(".")[1]]["sensor"])) for item in entity if state.get(entities[item.split(".")[1]]["sensor"]) is not None]) > SCRIPT_AIR_CLEANER_HELPER_PM_MINIMUM):
    homeassistant.turn_on(entity_id=helper)