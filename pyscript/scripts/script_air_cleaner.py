from config import *
from mapping import *
from settings import *
from helper import expr
from utils import *

import sys 

group = SCRIPT_AIR_CLEANER_GROUP
entities = SCRIPT_AIR_CLEANER_ENTITIES
sensors = SCRIPT_AIR_CLEANER_SENSOR
helper = SCRIPT_AIR_CLEANER_HELPER

retrigger_delay = SCRIPT_AIR_CLEANER_RETRIGGER_DELAY
clean_mode_percentage = SCRIPT_AIR_CLEANER_CLEAN_MODE_PERCENTAGE
sleep_mode_percentage = SCRIPT_AIR_CLEANER_SLEEP_MODE_PERCENTAGE

sleep_clean_delay = 1
helper_percentage_minimum = 50

@service
def script_air_cleaner():
  if state.get(group) != STATE_ON:
    script_air_cleaner_clean()
  else: 
    modes = [(state.getattr(entity).get(SCRIPT_AIR_CLEANER_ENTITY_MODE)) for entity in entities]
    if SCRIPT_AIR_CLEANER_PRESET_MODE_MANUAL in modes: 
      script_air_cleaner_sleep()
    else: 
      script_air_cleaner_turn_off()

# Trigger

@state_trigger(expr(entities, STATE_ON))
def script_air_cleaner_turned_on(entity=entities, var_name=None):
  script_air_cleaner_sleep(entity=var_name)

@task_unique("script_air_cleaner_threshold_on", kill_me=True)
@state_trigger(expr(sensors, SCRIPT_AIR_CLEANER_THRESHOLD_START, comparator=">"), watch=sensors)
@state_active(f"{EXPR_STATE_SEASON_POLLEN} and not {EXPR_STATE_OPEN_WINDOW}")
@time_active(EXPR_TIME_ACTIVE)
@log_context
def script_air_cleaner_threshold_on(var_name=None, ns=None, ctx=None):
  if state.get(var_name) != STATE_ON:
    script_air_cleaner_sleep()
    log(f"{var_name} with {value}pm2,5 above threshold {SCRIPT_AIR_CLEANER_THRESHOLD_START}", ns, ctx, "threshold:on")
  task.sleep(retrigger_delay)

@task_unique("script_air_cleaner_threshold_off", kill_me=True)
@state_trigger(expr(sensors, SCRIPT_AIR_CLEANER_THRESHOLD_STOP, comparator="<"), watch=sensors)
@state_active(EXPR_STATE_SEASON_POLLEN)
@time_active(EXPR_TIME_ACTIVE)
def script_air_cleaner_threshold_off(var_name=None, value=None, ns=None, ctx=None, **kwargs):
  if state.get(var_name) == STATE_ON:
    script_air_cleaner_turn_off()
    script_air_cleaner_turn_off(helper)
    log(f"{var_name} with {value} PM 2,5 below threshold {SCRIPT_AIR_CLEANER_THRESHOLD_STOP}", ns, ctx, "threshold:off")
  task.sleep(SCRIPT_AIR_CLEANER_RETRIGGER_DELAY)

# Functionality

@service
@log_context
def script_air_cleaner_clean(entity=entities, ctx=None, ns=None):
  if isinstance(entity, list): 
    for item in entity:
      script_air_cleaner_clean(entity=item)
  else:
    script_air_cleaner_sleep()
    task.sleep(sleep_clean_delay)
    pm = state.get(entity.replace("fan", "sensor")) # TODO: sensors in entity dict
    percentage = max(33, min(100, (int(pm) * 10)))
    fan.set_percentage(entity_id=entity, percentage=percentage)
    if percentage >= helper_percentage_minimum:
      script_air_cleaner_helper_air()
    log(f"clean: {percentage}% at {pm} pm2,5", ns, ctx, entity)

@state_trigger(expr(entities, STATE_ON))
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
      if int(str(entity_state.supported_features)) > 1:
        fan.set_preset_mode(entity_id=entity, preset_mode= SCRIPT_AIR_CLEANER_PRESET_MODE_SLEEP)
        log(f"sleep mode", ns, ctx, entity)
      else:
        fan.turn_on(entity_id=entity)
        fan.set_percentage(entity_id=entity, percentage=sleep_mode_percentage)
        log(f"sleep mode ({sleep_mode_percentage}%)", ns, ctx, entity)
  script_air_cleaner_turn_off(helper)

# Automation

@task_unique("script_air_cleaner_threshold_on", kill_me=True)
@state_trigger(expr(sensors, SCRIPT_AIR_CLEANER_THRESHOLD_START, comparator=">"), watch=sensors)
@state_active(EXPR_STATE_SEASON_POLLEN)
@time_active(EXPR_TIME_ACTIVE)
@log_context
def script_air_cleaner_threshold_on(var_name=None, ns=None, ctx=None):
  if state.get(var_name) != STATE_ON:
    script_air_cleaner_sleep()
    log(f"{value} pm2,5 above {SCRIPT_AIR_CLEANER_THRESHOLD_START} threshold", ns, ctx, var_name)
  task.sleep(retrigger_delay)

@task_unique("script_air_cleaner_threshold_off", kill_me=True)
@state_trigger(expr(sensors, SCRIPT_AIR_CLEANER_THRESHOLD_STOP, comparator="<"), watch=sensors, state_hold=SCRIPT_AIR_CLEANER_TIMEOUT_CLEAN)
@state_active(EXPR_STATE_SEASON_POLLEN)
@time_active(EXPR_TIME_ACTIVE)
def script_air_cleaner_threshold_off(var_name=None, value=None, ns=None, ctx=None, **kwargs):
  if state.get(var_name) == STATE_ON:
    script_air_cleaner_turn_off()
    script_air_cleaner_turn_off(helper)
    log(f"{value} pm2,5 below {SCRIPT_AIR_CLEANER_THRESHOLD_STOP} threshold", ns, ctx, var_name)
  task.sleep(SCRIPT_AIR_CLEANER_RETRIGGER_DELAY)

# Helper

# @state_trigger(expr(entities, STATE_ON))
# def script_air_cleaner_turn_on(entity=entities, var_name=None):
#   if isinstance(entity, list):
#     for item in entity:
#       script_air_cleaner_turn_on(item)
#   else:
#     script_air_cleaner_sleep(entity)

@service
def script_air_cleaner_turn_off(entity=entities):
  if isinstance(entity, list):
    for item in entity:
      script_air_cleaner_turn_off(item)
  else:
    pyscript.script_off_air(entity=entity)

@service
def script_air_cleaner_helper_air():
  for entity in helper:
    homeassistant.turn_on(entity_id=entity)

# Logging

@state_trigger(expr(entities, STATE_OFF))
@log_context
def script_air_cleaner_log_entity_turned_off(var_name=None, ns=None, ctx=None):
  pm = state.get(var_name.replace("fan", "sensor")) 
  log(f"turned off ({pm} pm2,5)", ns, ctx, var_name)

# Timeout

@state_trigger(expr(entities, STATE_ON), state_hold=SCRIPT_AIR_CLEANER_TIMEOUT_CLEAN)
def script_air_cleaner_timeout(var_name=None):
  script_air_cleaner_sleep(var_name)
  script_air_cleaner_turn_off(helper)