from helper import expr
from constants import STATES_HA_UNDEFINED

import random

ENTITIES_LOCATION = [ 
  "device_tracker.iphone", 
  "device_tracker.iphone_2", 
  "device_tracker.iphone_privat" 
]

CLEANER = "vaccum.staubsauger"

@time_active("cron(* 9-19 * * 1-6)")
@state_trigger(expr(ENTITIES_LOCATION))
def on_location_changed(cleane=CLEANER, var_name=False, value=None, old_value=None, **kwargs):
  
  # Multiple devices report the state
  if ( ( ENTITIES_LOCATION[0] == value and ENTITIES_LOCATION[1] == value ) or 
       ( ENTITIES_LOCATION[0] == value and ENTITIES_LOCATION[2] == value ) or 
       ( ENTITIES_LOCATION[1] == value and ENTITIES_LOCATION[2] == value ) ): 
 
    if value == "HOME": # Better: distance
      vacuum.stop(entity_id=CLEANER)
      vacuum.return_to_dock(entity_id=CLEANER)
      
    elif value == "AWAY":
      vacuum.start(entity_id=CLEANER)