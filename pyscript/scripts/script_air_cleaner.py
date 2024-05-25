from constants import *
from utils import *

import sys 

group = SCRIPT_AIR_CLEANER_GROUP
entities = SCRIPT_AIR_CLEANER_ENTITIES
sensors = SCRIPT_AIR_CLEANER_SENSOR
helper = SCRIPT_AIR_CLEANER_HELPER

clean_mode_percentage = SCRIPT_AIR_CLEANER_CLEAN_MODE_PERCENTAGE
sleep_mode_percentage = SCRIPT_AIR_CLEANER_SLEEP_MODE_PERCENTAGE
helper_pm_minimum = SCRIPT_AIR_CLEANER_HELPER_PM_MINIMUM
retrigger_delay = SCRIPT_AIR_CLEANER_THRESHOLD_RETRIGGER_DELAY
wait_active_delay = SCRIPT_AIR_CLEANER_WAIT_ACTIVE_DELAY

# Service

@service
def script_air_cleaner():
  if int(state.get(f"{group}.percentage")) <= sleep_mode_percentage:
    script_air_cleaner_clean()
  else: 
    script_air_cleaner_sleep()

# Automation

@task_unique("script_air_cleaner_threshold_on", kill_me=True)
@state_trigger(expr(sensors, SCRIPT_AIR_CLEANER_THRESHOLD_START, comparator=">"), watch=sensors)
@state_active(f"{EXPR_STATE_SEASON_POLLEN} and not {EXPR_STATE_OPEN_WINDOW}")
@time_active(EXPR_TIME_ACTIVE)
@log_context
def script_air_cleaner_threshold_on(var_name=None, value=None, ns=None, ctx=None):
  if state.get(var_name) != STATE_ON:
    script_air_cleaner_sleep()
    log(f"{var_name} with {value}pm2,5 above threshold {SCRIPT_AIR_CLEANER_THRESHOLD_START}", ns, ctx, "threshold:on")
  task.sleep(retrigger_delay)

@task_unique("script_air_cleaner_threshold_off", kill_me=True)
@state_trigger(expr(sensors, SCRIPT_AIR_CLEANER_THRESHOLD_STOP, comparator="<"), watch=sensors)
@state_active(f"{EXPR_STATE_SEASON_POLLEN} and {group} == STATE_ON")
@time_active(EXPR_TIME_ACTIVE)
def script_air_cleaner_threshold_off(var_name=None, value=None, ns=None, ctx=None, **kwargs):
  if state.get(var_name) == STATE_ON:
    script_air_cleaner_turn_off()
    script_air_cleaner_turn_off(helper)
    log(f"{var_name} with {value} PM 2,5 below threshold {SCRIPT_AIR_CLEANER_THRESHOLD_STOP}", ns, ctx, "threshold:off")
  task.sleep(retrigger_delay)

# Functionality

@event_trigger(EVENT_NEVER)
@task_unique(group, kill_me=False)
@service
def script_air_cleaner_clean(entity=entities):
  fan.turn_on(entity_id=entity)
  if isinstance(entity, list): 
    for item in entity:
      task.sleep(wait_active_delay)
      script_air_cleaner_clean(entity=item)
    script_air_cleaner_helper_air()
  else:
    fan.set_percentage(entity_id=entity, percentage=script_air_cleaner_get_clean_percentage(entity))

@state_trigger(expr(entities, STATE_ON))
@state_trigger(expr(f"{group}.percentage", sleep_mode_percentage, comparator='>'), state_hold=SCRIPT_AIR_CLEANER_TIMEOUT_CLEAN)
@task_unique(group, kill_me=True)
@service
def script_air_cleaner_sleep(entity=entities, var_name=None, value=STATE_ON, ns=None, ctx=None):
  if var_name != None: entity = var_name # called by state trigger
  if value == STATE_OFF: return
  if isinstance(entity, list): 
    for item in entity:
      script_air_cleaner_sleep(entity=item)
  else: 
    entity_state = state.get(entity)
    if entity_state: 
      if entity_state.supported_features > 1:
        fan.set_preset_mode(entity_id=entity, preset_mode= SCRIPT_AIR_CLEANER_PRESET_MODE_SLEEP)
      else:
        fan.turn_on(entity_id=entity)
        fan.set_percentage(entity_id=entity, percentage=sleep_mode_percentage)

  script_air_cleaner_turn_off(helper)

# Helper

@service
def script_air_cleaner_turn_off(entity=entities):
  if isinstance(entity, list):
    for item in entity:
      script_air_cleaner_turn_off(item)
  else:
    pyscript.script_off_air(entity=entity)

@log_context
def script_air_cleaner_get_clean_percentage(entity, ns=None, ctx=None):
  pm = state.get(entity.replace("fan", "sensor"))
  percentage = max(clean_mode_percentage, min(100, (int(pm) * 10)))
  log(f"{percentage}% at {pm} pm2,5", ns, ctx, entity)
  return percentage

def script_air_cleaner_helper_air(entity=entities):
  pm_total = sum([int(state.get(item.replace("fan", "sensor"))) for item in entity])
  if pm_total > helper_pm_minimum:
    for item in helper:
      homeassistant.turn_on(entity_id=entity)