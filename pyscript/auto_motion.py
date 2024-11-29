from constants.entities import ENTITIES_MOTION
from constants.expressions import EXPR_TIME_MOTION_DAY
from constants.mappings import STATE_ON, STATE_OFF
from constants.settings import SET_MOTION_TIMEOUT

from utils import *

trigger = []

def on_motion_factory(entity):

  @state_trigger(expr(entity, STATE_ON), state_hold_false=0)
  @time_active((f"range(sunset - {ENTITIES_MOTION.get(entity)['sun_diff']}min, sunrise + {ENTITIES_MOTION.get(entity)['sun_diff']}min)" if 'sun_diff' in ENTITIES_MOTION.get(entity) else EXPR_TIME_MOTION_DAY))
  @debugged
  def on_motion(var_name=None): 
    scene.turn_on(entity_id=ENTITIES_MOTION.get(var_name, {}).get("on"), transition=0)
  trigger.append(on_motion) 

def off_motion_factory(entity):
#
  @state_trigger(expr(entity, STATE_OFF), state_hold=SET_MOTION_TIMEOUT)
  def off_motion(var_name=None):
    transition = float(ENTITIES_MOTION.get(var_name, {}).get("transition", 0))
    scene.turn_on(entity_id=ENTITIES_MOTION.get(var_name, {}).get("off"), transition=transition)
  trigger.append(off_motion)

for entity in ENTITIES_MOTION:
  on_motion_factory(entity)
  off_motion_factory(entity)
