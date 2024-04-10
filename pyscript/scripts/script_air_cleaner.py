from config import (
  EXPR_TIME_ACTIVE, EXPR_TIME_SEASON_POLLEN, 
  SCRIPT_AIR_CLEANER_THRESHOLD_START, SCRIPT_AIR_CLEANER_THRESHOLD_STOP,
  SCRIPT_AIR_CLEANER_PERCENTAGE_CLEAN, SCRIPT_AIR_CLEANER_TIMEOUT_CLEAN
)
from mapping import (
  STATE_ON, SCRIPT_AIR_CLEANER_ENTITY, 
  SCRIPT_AIR_CLEANER_ENTITY_ATTRIBUTE, SCRIPT_AIR_CLEANER_ENTITY_MODE, 
  SCRIPT_AIR_CLEANER_HELPER, SCRIPT_AIR_CLEANER_SENSOR, 
  SCRIPT_AIR_CLEANER_PRESET_MODE_MANUAL, SCRIPT_AIR_CLEANER_PRESET_MODE_SLEEP
)
from helper import expr
from utils import log, log_func

entity = SCRIPT_AIR_CLEANER_ENTITY

@service
@log_func
def script_air_cleaner():
  
  if state.get(entity) == STATE_ON:
    mode = state.getattr(entity).get(SCRIPT_AIR_CLEANER_ENTITY_MODE)
    
    if mode == SCRIPT_AIR_CLEANER_PRESET_MODE_SLEEP:
      script_air_cleaner_turn_off()
    else: 
      script_air_cleaner_mode_sleep()
  else:
    script_air_cleaner_automation(mode=SCRIPT_AIR_CLEANER_PRESET_MODE_MANUAL)

# Trigger
    
@state_trigger(expr(entity, STATE_ON))
def script_air_cleaner_automation(mode=None):
  script_air_cleaner_mode_sleep()
  if mode == SCRIPT_AIR_CLEANER_PRESET_MODE_MANUAL: 
    await task.sleep(3)
    script_air_cleaner_automation_clean()
    
@time_active(EXPR_TIME_ACTIVE)
@state_active(EXPR_TIME_SEASON_POLLEN)
@state_trigger(f"int({SCRIPT_AIR_CLEANER_SENSOR}) > {SCRIPT_AIR_CLEANER_THRESHOLD_START}")
@log_func
def script_air_cleaner_threshold_on():
  if state.get(entity) != STATE_ON:
    script_air_cleaner_turn_on()

@time_active(EXPR_TIME_ACTIVE)
@state_active(EXPR_TIME_SEASON_POLLEN)
@state_trigger(f"int({SCRIPT_AIR_CLEANER_SENSOR}) < {SCRIPT_AIR_CLEANER_THRESHOLD_STOP}")
@log_func
def script_air_cleaner_threshold_off():
  if state.get(entity) == STATE_ON:
    script_air_cleaner_turn_off()

# Helper

def script_air_cleaner_turn_on():
    if state.get(entity) != STATE_ON:
      script_air_cleaner_mode_sleep()

def script_air_cleaner_turn_off(entity=SCRIPT_AIR_CLEANER_ENTITY):
  pyscript.script_off_air(entity=[entity])

# Functionality

def script_air_cleaner_mode_sleep():
  fan.set_preset_mode(entity_id=entity, preset_mode=SCRIPT_AIR_CLEANER_PRESET_MODE_SLEEP)

@service
@log_func
def script_air_cleaner_automation_clean():
  fan.set_percentage(entity_id=entity, percentage=SCRIPT_AIR_CLEANER_PERCENTAGE_CLEAN)

# Timeout

@state_trigger(expr(entity, STATE_ON) and f"{entity}.{SCRIPT_AIR_CLEANER_ENTITY_ATTRIBUTE} == '{SCRIPT_AIR_CLEANER_PRESET_MODE_MANUAL}'", state_hold=SCRIPT_AIR_CLEANER_TIMEOUT_CLEAN)
@log_func
def script_air_cleaner_timeout():
  script_air_cleaner_mode_sleep()
  script_air_cleaner_turn_off(SCRIPT_AIR_CLEANER_HELPER)