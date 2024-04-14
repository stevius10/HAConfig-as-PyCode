from config import (
  EXPR_TIME_ACTIVE, EXPR_TIME_SEASON_POLLEN, SCRIPT_AIR_CLEANER_RETRIGGER_DELAY,
  SCRIPT_AIR_CLEANER_THRESHOLD_START, SCRIPT_AIR_CLEANER_THRESHOLD_STOP,
  SCRIPT_AIR_CLEANER_PERCENTAGE_CLEAN, SCRIPT_AIR_CLEANER_TIMEOUT_CLEAN, 
  SCRIPT_AIR_CLEANER_TIMEOUT_HELPER
)
from mapping import (
  STATE_ON, SCRIPT_AIR_CLEANER_ENTITY, 
  SCRIPT_AIR_CLEANER_ENTITY_ATTRIBUTE, SCRIPT_AIR_CLEANER_ENTITY_MODE, 
  SCRIPT_AIR_CLEANER_HELPER, SCRIPT_AIR_CLEANER_SENSOR, 
  SCRIPT_AIR_CLEANER_PRESET_MODE_MANUAL, SCRIPT_AIR_CLEANER_PRESET_MODE_SLEEP,
  SCRIPT_AIR_CLEANER_SENSOR_SPEED, SCRIPT_AIR_CLEANER_SPEED_THRESHOLD
)
from helper import expr
from utils import log

import sys 
entity = SCRIPT_AIR_CLEANER_ENTITY

@service
def script_air_cleaner():
  if state.get(entity) == STATE_ON:    
    if state.getattr(entity).get(SCRIPT_AIR_CLEANER_ENTITY_MODE) == SCRIPT_AIR_CLEANER_PRESET_MODE_SLEEP:
      script_air_cleaner_turn_off()
    else: 
      script_air_cleaner_mode_sleep()
  else:
    script_air_cleaner_automation(mode=SCRIPT_AIR_CLEANER_PRESET_MODE_MANUAL)

# Trigger

@state_trigger(expr(entity, STATE_ON))
@task_unique("script_air_cleaner_automation", kill_me=True)
def script_air_cleaner_automation(mode=None):
  script_air_cleaner_mode_sleep()
  if mode == SCRIPT_AIR_CLEANER_PRESET_MODE_MANUAL: 
    await task.sleep(3)
    script_air_cleaner_automation_clean()
  task.sleep(SCRIPT_AIR_CLEANER_RETRIGGER_DELAY)

@time_active(EXPR_TIME_ACTIVE)
@state_active(EXPR_TIME_SEASON_POLLEN)
@state_trigger(expr(SCRIPT_AIR_CLEANER_SENSOR, SCRIPT_AIR_CLEANER_THRESHOLD_START, comparator=">"))
@task_unique("script_air_cleaner_threshold_on", kill_me=True)
def script_air_cleaner_threshold_on():
  if state.get(entity) != STATE_ON:
    script_air_cleaner_turn_on()
  task.sleep(SCRIPT_AIR_CLEANER_RETRIGGER_DELAY)

@time_active(EXPR_TIME_ACTIVE)
@state_active(EXPR_TIME_SEASON_POLLEN)
@state_trigger(expr(SCRIPT_AIR_CLEANER_SENSOR_SPEED, SCRIPT_AIR_CLEANER_SPEED_THRESHOLD, comparator=">"), state_hold=SCRIPT_AIR_CLEANER_TIMEOUT_CLEAN)
@state_trigger(expr(SCRIPT_AIR_CLEANER_SENSOR, SCRIPT_AIR_CLEANER_THRESHOLD_STOP, comparator="<"))
@task_unique("script_air_cleaner_threshold_off", kill_me=True)
def script_air_cleaner_automation_off():
  if state.get(entity) == STATE_ON:
    script_air_cleaner_turn_off()
  task.sleep(SCRIPT_AIR_CLEANER_RETRIGGER_DELAY)

# Helper

def script_air_cleaner_turn_on():
    if state.get(entity) != STATE_ON:
      script_air_cleaner_mode_sleep()
      
def script_air_cleaner_turn_off(entity=SCRIPT_AIR_CLEANER_ENTITY):
  pyscript.script_off_air(entity=[entity])

# Functionality

def script_air_cleaner_mode_sleep():
  fan.set_preset_mode(entity_id=entity, preset_mode=SCRIPT_AIR_CLEANER_PRESET_MODE_SLEEP)

def script_air_cleaner_automation_clean():
  fan.set_percentage(entity_id=entity, percentage=SCRIPT_AIR_CLEANER_PERCENTAGE_CLEAN)
  for helper in SCRIPT_AIR_CLEANER_HELPER:
    homeassistant.turn_on(entity_id=helper)

# Timeout

@state_trigger(expr(entity, STATE_ON) and f"{entity}.{SCRIPT_AIR_CLEANER_ENTITY_ATTRIBUTE} == '{SCRIPT_AIR_CLEANER_PRESET_MODE_MANUAL}'", state_hold=SCRIPT_AIR_CLEANER_TIMEOUT_CLEAN)
def script_air_cleaner_timeout():
  script_air_cleaner_mode_sleep()
  for helper in SCRIPT_AIR_CLEANER_HELPER:
    homeassistant.turn_off(entity_id=helper)

# @state_trigger(expr(SCRIPT_AIR_CLEANER_HELPER, STATE_ON), state_hold=SCRIPT_AIR_CLEANER_TIMEOUT_HELPER)
# def script_air_cleaner_timeout_helper():
#   script_air_cleaner_mode_sleep()
#   for helper in SCRIPT_AIR_CLEANER_HELPER:
#     homeassistant.turn_off(entity_id=helper)