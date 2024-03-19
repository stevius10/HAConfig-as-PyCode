from helper import expr
from constants import DAYTIME, TIME_DATE_RANGE_AIR_CLEANER, SCRIPT_AIR_CLEANER_THRESHOLD
from mapping import SCRIPT_AIR_CLEANER_PRESET_MODE_MANUAL, SCRIPT_AIR_CLEANER_PRESET_MODE_SLEEP
from naming import STATE_ON, SCRIPT_AIR_CLEANER_ENTITY, \
  SCRIPT_AIR_CLEANER_ENTITY_ATTRIBUTE, SCRIPT_AIR_CLEANER_ENTITY_MODE, \
  SCRIPT_AIR_CLEANER_HELPER, SCRIPT_AIR_CLEANER_SENSOR
from timeout import SCRIPT_AIR_CLEANER_TIMEOUT_AUTOMATION, SCRIPT_AIR_CLEANER_TIMEOUT_SLEEP

entity = SCRIPT_AIR_CLEANER_ENTITY
entity_attribute = SCRIPT_AIR_CLEANER_ENTITY_ATTRIBUTE
helper = SCRIPT_AIR_CLEANER_HELPER 
sensor = SCRIPT_AIR_CLEANER_SENSOR

@service
def script_air_cleaner():
  if state.get(entity) == "on":
    mode = state.getattr(entity).get(SCRIPT_AIR_CLEANER_ENTITY_MODE)
    
    if mode == "sleep":
      script_air_cleaner_turn_off()
      
    if mode == "manual": 
      fan.set_preset_mode(entity_id=entity, preset_mode=SCRIPT_AIR_CLEANER_PRESET_MODE_SLEEP)

  else:
    script_air_cleaner_mode_sleep()

# Trigger
@state_trigger(expr(entity, "on"))
def script_air_cleaner_turn_on():
  script_air_cleaner_mode_sleep()

@time_active(DAYTIME and TIME_DATE_RANGE_AIR_CLEANER)
@state_trigger(f"{state.get(SCRIPT_AIR_CLEANER_SENSOR)} > {SCRIPT_AIR_CLEANER_THRESHOLD}", watch=[SCRIPT_AIR_CLEANER_SENSOR])
def script_air_cleaner_threshold_on(entity=SCRIPT_AIR_CLEANER_ENTITY):
  script_air_cleaner_turn_on()

@time_active(DAYTIME and TIME_DATE_RANGE_AIR_CLEANER)
@state_trigger(f"{state.get(SCRIPT_AIR_CLEANER_SENSOR)} <= 5", watch=[SCRIPT_AIR_CLEANER_SENSOR]) 
def script_air_cleaner_threshold_off(entity=SCRIPT_AIR_CLEANER_ENTITY):
  script_air_cleaner_turn_off()

# Helper

def script_air_cleaner_turn_off(entity=SCRIPT_AIR_CLEANER_ENTITY):
  pyscript.script_off_air(entity=[entity])

# Functionality

def script_air_cleaner_mode_sleep():
  fan.set_preset_mode(entity_id=entity, preset_mode=SCRIPT_AIR_CLEANER_PRESET_MODE_SLEEP)

@service
def script_air_cleaner_automation_clean():
  fan.set_percentage(entity_id=entity, percentage=SCRIPT_AIR_CLEANER_PERCENTAGE_MAX)
  switch.turn_on(SCRIPT_AIR_CLEANER_HELPER)


# Timeout

@state_trigger(expr(entity, STATE_ON) and f"{entity}.{SCRIPT_AIR_CLEANER_ENTITY_ATTRIBUTE} == {SCRIPT_AIR_CLEANER_PRESET_MODE_MANUAL}", state_hold=SCRIPT_AIR_CLEANER_TIMEOUT_AUTOMATION)
def script_air_cleaner_timeout():
  script_air_cleaner_mode_sleep()
  script_air_cleaner_turn_off(SCRIPT_AIR_CLEANER_HELPER)

# todo: remove after auto_timeout
@state_trigger(expr(entity, STATE_ON) and f"{entity}.{SCRIPT_AIR_CLEANER_ENTITY_ATTRIBUTE} == {SCRIPT_AIR_CLEANER_PRESET_MODE_SLEEP}", state_hold=SCRIPT_AIR_CLEANER_TIMEOUT_SLEEP)
def script_air_cleaner_timeout():
  script_air_cleaner_turn_off() 


'''
SCRIPT_AIR_CLEANER_PERCENTAGE_MAX = 100
SCRIPT_AIR_CLEANER_PERCENTAGE_MEDIUM = 67
SCRIPT_AIR_CLEANER_PERCENTAGE_MIN = 33

  percentage = state.get(entity, SCRIPT_AIR_CLEANER_ENTITY_ATTRIBUTE)
  if percentage > SCRIPT_AIR_CLEANER_PERCENTAGE_MEDIUM: pass
  elif percentage > SCRIPT_AIR_CLEANER_PERCENTAGE_MIN: pass
  elif percentage > 0: pass
  else: pass
'''