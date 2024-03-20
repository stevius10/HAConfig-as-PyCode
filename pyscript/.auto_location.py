from helper import expr
from constants import STATES_HA_UNDEFINED

ENTITIES_LOCATION = [ 
  "device_tracker.iphone", 
  "device_tracker.iphone_privat",
  "device_tracker.watch_icloud"
]

ENTITY_HOME_DISTANCE_ORIGIN = "sensor.h_distance_iphone_ipad"

ENTITIES_LOCATION_STATE_HOME = "home"

DAYTIME = "cron(* 9-19 * * 1-6)"
CLEANER = "vaccum.staubsauger"

meter_per_minute = 60

# Less false-positive
@time_active(DAYTIME)
@state_trigger(expr(ENTITIES_LOCATION, "!= {ENTITIES_LOCATION_STATE_HOME}", operator="and"))
def on_location_changed(cleaner=CLEANER, var_name=False, value=None, old_value=None, **kwargs):
  
  # Multiple devices report the state
  for entity in ENTITIES_LOCATION:
    if (state.get(entity) != ENTITIES_LOCATION_STATE_HOME):
      return 0
  
    vacuum.start(entity_id=CLEANER)
    pyscript.turn_off()

@time_active(DAYTIME)
@state_trigger(f"int({ENTITY_HOME_DISTANCE_ORIGIN}) < 500", watch=[ENTITY_HOME_DISTANCE_ORIGIN]) # Implement trend sensor
def on_way_home(cleaner=CLEANER, var_name=False, value=None, old_value=None, **kwargs):
  distance_now = state.get(ENTITY_HOME_DISTANCE_ORIGIN)
  await task.sleep(120) # conflict: icloud periode 30m
  distance_after = state.get(ENTITY_HOME_DISTANCE_ORIGIN)
  
  if distance_after < distance_now + meter_per_minute:
    vacuum.stop(entity_id=cleaner)
    vacuum.return_to_dock(entity_id=cleaner)