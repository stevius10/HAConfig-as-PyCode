from constants import *
from utils import *

entities = SCRIPT_AIR_CLEANER_ENTITIES

clean_mode_percentage = SCRIPT_AIR_CLEANER_CLEAN_MODE_PERCENTAGE
sleep_mode_percentage = SCRIPT_AIR_CLEANER_SLEEP_MODE_PERCENTAGE
helper_pm_minimum = SCRIPT_AIR_CLEANER_HELPER_PM_MINIMUM
retrigger_delay = SCRIPT_AIR_CLEANER_THRESHOLD_RETRIGGER_DELAY
wait_active_delay = SCRIPT_AIR_CLEANER_WAIT_ACTIVE_DELAY

@task_unique("script_air_cleaner_threshold_on", kill_me=True)
@state_trigger(expr([entity["sensor"] for entity in entities.values()], SCRIPT_AIR_CLEANER_THRESHOLD_START, comparator=">"), watch=[entity["sensor"] for entity in entities.values()])
@state_active(f"{EXPR_STATE_AIR_THRESHOLD_SEASON} and not {EXPR_STATE_OPEN_WINDOW}")
@time_active(EXPR_STATE_AIR_THRESHOLD_TIME)
@log_context
def script_air_cleaner_threshold_on(var_name=None, value=None, ns=None, ctx=None):
  entity = entities[var_name.split(".")[1]]["fan"]
  if state.get(entity) != STATE_ON:
    script_air_cleaner_sleep(entity) 
    log(f"{entity} with {var_name} got {value} PM 2,5 above threshold {SCRIPT_AIR_CLEANER_THRESHOLD_START}", ns, ctx, "threshold:on")
  task.sleep(retrigger_delay)

@task_unique("script_air_cleaner_threshold_off", kill_me=True)  
@state_trigger(expr([entity["sensor"] for entity in entities.values()], SCRIPT_AIR_CLEANER_THRESHOLD_STOP, comparator="<"), watch=[entity["sensor"] for entity in entities.values()])
@state_active(f"{EXPR_STATE_AIR_THRESHOLD_SEASON} and {[entity['fan'] for entity in entities.values()]} == STATE_ON")
@time_active(EXPR_STATE_AIR_THRESHOLD_TIME)
def script_air_cleaner_threshold_off(var_name=None, value=None, ns=None, ctx=None, **kwargs):
  entity = entities[var_name.split(".")[1]]["fan"]
  if state.get(var_name) == STATE_ON:
    script_air_cleaner_turn_off(entity)
    log(f"{entity} with {var_name} got {value} PM 2,5 below threshold {SCRIPT_AIR_CLEANER_THRESHOLD_STOP}", ns, ctx, "threshold:off")
  task.sleep(retrigger_delay)

@event_trigger(EVENT_NEVER)
@task_unique("-".join([entity["fan"] for entity in entities.values()]), kill_me=False)
@service
def script_air_cleaner_clean(entity=[entity["fan"] for entity in entities.values()]):
  fan.turn_on(entity_id=entity)
  if isinstance(entity, list):
    for item in entity:
      task.sleep(wait_active_delay)
      script_air_cleaner_clean(entity=item)
    script_air_cleaner_helper_air(check=True)
  else:
    fan.set_percentage(entity_id=entity, percentage=script_air_cleaner_get_clean_percentage(entity))

@state_trigger(expr([entity["fan"] for entity in entities.values()], STATE_ON))
@state_trigger(expr([entity['percentage'] for entity in entities.values()], sleep_mode_percentage, comparator='>'), state_hold=SCRIPT_AIR_CLEANER_TIMEOUT_CLEAN)
@task_unique("-".join([entity["fan"] for entity in entities.values()]), kill_me=False)
@service
def script_air_cleaner_sleep(entity=[entity["fan"] for entity in entities.values()], var_name=None, value=STATE_ON, ns=None, ctx=None):
  if var_name != None: entity = var_name
  if value == STATE_OFF: return
  if isinstance(entity, list):
    for item in entity:
      script_air_cleaner_sleep(entity=item)
  else:
    supported_features = int(state.get(f"{entity}.supported_features")) if state.get(entity) else None
    if supported_features == 9: fan.set_preset_mode(entity_id=entity, preset_mode=SCRIPT_AIR_CLEANER_PRESET_MODE_SLEEP)
    elif supported_features == 1:
      fan.turn_on(entity_id=entity)
      fan.set_percentage(entity_id=entity, percentage=sleep_mode_percentage)
  script_air_cleaner_turn_off([entity["luftung"] for entity in entities.values()])

@service
def script_air_cleaner_turn_off(entity=[entity["fan"] for entity in entities.values()]):
  if isinstance(entity, list):
    for item in entity:
      script_air_cleaner_turn_off(item)
  else:
    pyscript.script_off_air(entity=entity)

@log_context
def script_air_cleaner_get_clean_percentage(entity, ns=None, ctx=None):
  for key, value in entities.items():
    if value["fan"] == entity:
      pm = state.get(value["sensor"])
      break
  percentage = max(clean_mode_percentage, min(100, (int(pm) * 10)))
  log(f"{percentage}% at {pm} pm2,5", ns, ctx, entity)
  return percentage

@service
def script_air_cleaner_helper_air(entity=[entity["fan"] for entity in entities.values()], helper=[entity["luftung"] for entity in entities.values()], check=False):
  if (check == False) or sum(int(state.get(entities[item.split(".")[1]]["sensor"])) for item in entity if state.get(entities["sensor"]) is not None):
    for item in helper:
      homeassistant.turn_on(entity_id=item)


# from constants import *
# from utils import *

# group = SCRIPT_AIR_CLEANER_GROUP
# entities = SCRIPT_AIR_CLEANER_ENTITIES
# sensors = SCRIPT_AIR_CLEANER_SENSOR
# helpers = SCRIPT_AIR_CLEANER_HELPER

# clean_mode_percentage = SCRIPT_AIR_CLEANER_CLEAN_MODE_PERCENTAGE
# sleep_mode_percentage = SCRIPT_AIR_CLEANER_SLEEP_MODE_PERCENTAGE
# helper_pm_minimum = SCRIPT_AIR_CLEANER_HELPER_PM_MINIMUM
# retrigger_delay = SCRIPT_AIR_CLEANER_THRESHOLD_RETRIGGER_DELAY
# wait_active_delay = SCRIPT_AIR_CLEANER_WAIT_ACTIVE_DELAY

# # Automation

# @task_unique("script_air_cleaner_threshold_on", kill_me=True)
# @state_trigger(expr(sensors, SCRIPT_AIR_CLEANER_THRESHOLD_START, comparator=">"), watch=sensors)
# @state_active(f"{EXPR_STATE_AIR_THRESHOLD_SEASON} and not {EXPR_STATE_OPEN_WINDOW}")
# @time_active(EXPR_TIME_AVTIVE_THRESHOLDS)
# @log_context
# def script_air_cleaner_threshold_on(var_name=None, value=None, ns=None, ctx=None):
#   if state.get(var_name) != STATE_ON:
#     script_air_cleaner_sleep()
#     log(f"{var_name} with {value}pm2,5 above threshold {SCRIPT_AIR_CLEANER_THRESHOLD_START}", ns, ctx, "threshold:on")
#   task.sleep(retrigger_delay)

# @task_unique("script_air_cleaner_threshold_off", kill_me=True)
# @state_trigger(expr(sensors, SCRIPT_AIR_CLEANER_THRESHOLD_STOP, comparator="<"), watch=sensors)
# @state_active(f"{EXPR_STATE_AIR_THRESHOLD_SEASON} and {group} == STATE_ON")
# @time_active(EXPR_TIME_AVTIVE_THRESHOLDS)
# def script_air_cleaner_threshold_off(var_name=None, value=None, ns=None, ctx=None, **kwargs):
#   if state.get(var_name) == STATE_ON:
#     script_air_cleaner_turn_off(var_name)
#     script_air_cleaner_turn_off(helpers)
#     log(f"{var_name} with {value} PM 2,5 below threshold {SCRIPT_AIR_CLEANER_THRESHOLD_STOP}", ns, ctx, "threshold:off")
#   task.sleep(retrigger_delay)

# # Functionality

# @event_trigger(EVENT_NEVER)
# @task_unique(group, kill_me=False)
# @service
# def script_air_cleaner_clean(entity=entities):
#   fan.turn_on(entity_id=entity)
#   if isinstance(entity, list): 
#     for item in entity:
#       task.sleep(wait_active_delay)
#       script_air_cleaner_clean(entity=item)
#     script_air_cleaner_helper_air(check=True)
#   else:
#     fan.set_percentage(entity_id=entity, percentage=script_air_cleaner_get_clean_percentage(entity))

# @state_trigger(expr(entities, STATE_ON))
# @state_trigger(expr(f"{group}.percentage", sleep_mode_percentage, comparator='>'), state_hold=SCRIPT_AIR_CLEANER_TIMEOUT_CLEAN)
# @task_unique(group, kill_me=True)
# @service
# def script_air_cleaner_sleep(entity=entities, var_name=None, value=STATE_ON, ns=None, ctx=None):
#   if var_name != None: entity = var_name # called by state trigger
#   if value == STATE_OFF: return
#   if isinstance(entity, list): 
#     for item in entity:
#       script_air_cleaner_sleep(entity=item)
#   else:
#     supported_features = int(state.get(f"{entity}.supported_features")) if state.get(entity) else None
#     if supported_features == 9: fan.set_preset_mode(entity_id=entity, preset_mode=SCRIPT_AIR_CLEANER_PRESET_MODE_SLEEP)
#     elif supported_features == 1:
#       fan.turn_on(entity_id=entity)
#       fan.set_percentage(entity_id=entity, percentage=sleep_mode_percentage)
#   script_air_cleaner_turn_off(helpers)

# # Helper

# @service
# def script_air_cleaner_turn_off(entity=entities):
#   if isinstance(entity, list):
#     for item in entity:
#       script_air_cleaner_turn_off(item)
#   else:
#     pyscript.script_off_air(entity=entity)

# @log_context
# def script_air_cleaner_get_clean_percentage(entity, ns=None, ctx=None):
#   pm = state.get(entity.replace("fan", "sensor"))
#   percentage = max(clean_mode_percentage, min(100, (int(pm) * 10)))
#   log(f"{percentage}% at {pm} pm2,5", ns, ctx, entity)
#   return percentage

# @service # without check 
# def script_air_cleaner_helper_air(entity=entities, helper=helpers, check=False):
#   if (check == False) or (sum([int(state.get(item.replace("fan", "sensor"))) for item in entity]) > helper_pm_minimum):
#     for item in helper:
#       homeassistant.turn_on(entity_id=item)