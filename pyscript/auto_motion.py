from constants.entities import AUTO_MOTION_ENTITIES
from constants.expressions import EXPR_TIME_RANGE_DAY_MOTION
from constants.mappings import STATE_ON, STATE_OFF
from constants.settings import AUTO_MOTION_TIMEOUT

from utils import *

trigger = []

def on_motion_factory(entity):

  @state_trigger(expr(entity, STATE_ON))
  @time_active((f"range(sunset - {AUTO_MOTION_ENTITIES.get(entity)['sun_diff']}min, sunrise + {AUTO_MOTION_ENTITIES.get(entity)['sun_diff']}min)" if 'sun_diff' in AUTO_MOTION_ENTITIES.get(entity) else EXPR_TIME_RANGE_DAY_MOTION))
  @debugged
  def on_motion(var_name=None): 
    scene.turn_on(entity_id=AUTO_MOTION_ENTITIES.get(var_name, {}).get("on"), transition=0)
  trigger.append(on_motion) 

def off_motion_factory(entity):

  @state_trigger(expr(entity, STATE_OFF), state_hold=AUTO_MOTION_TIMEOUT)
  @debugged
  def off_motion(var_name=None):
    transition = float(AUTO_MOTION_ENTITIES.get(var_name, {}).get("transition", 0))
    scene.turn_on(entity_id=AUTO_MOTION_ENTITIES.get(var_name, {}).get("off"), transition=transition)
  trigger.append(off_motion)

for entity in AUTO_MOTION_ENTITIES:
  on_motion_factory(entity)
  off_motion_factory(entity)

# Higher computational complexity in favor of readability
#
# from constants import *
# from utils import expr
#
# motion_trigger = []
# entities = AUTO_MOTION_ENTITIES
#
# # motion: motion detected
# def on_motion_factory(entity):
#
#   @state_trigger(expr(entity, STATE_ON), state_check_now=True)
#   @time_active((f"range(sunset - {entities.get(entity)['sun_diff']}min, sunrise + {entities.get(entity)['sun_diff']}min)" if 'sun_diff' in entities.get(entity) else EXPR_TIME_RANGE_DAY))
#   # @log_func
#   def on_motion(var_name=None): 
#     if var_name in entities and "on" in entities.get(var_name):
#       transition = 0 # float(entities.get(var_name).get("transition")) if entities.get(var_name).get("transition") else 0
#       scene.turn_on(entity_id=entities.get(var_name).get("on"), transition=transition)
#   motion_trigger.append(on_motion) 
#
# # motion: no motion detected
# def off_motion_factory(entity):
#
#   @state_trigger(expr(entity, STATE_OFF), state_hold=AUTO_MOTION_TIMEOUT, state_check_now=True)
#   # @log_func
#   def off_motion(var_name=None):
#     if var_name in entities and "off" in entities.get(var_name):
#       transition = float(entities.get(var_name).get("transition")) if entities.get(var_name).get("transition") else 0
#       scene.turn_on(entity_id=entities.get(var_name).get("off"), transition=transition)
#   motion_trigger.append(off_motion)
#
# for entity in entities:
#   on_motion_factory(entity)
#   off_motion_factory(entity)