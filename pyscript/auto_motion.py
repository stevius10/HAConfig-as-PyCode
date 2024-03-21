from config import AUTO_MOTION_TIMEOUT, EXPR_TIME_RANGE_DAY
from entities import AUTO_MOTION_ENTITIES
from helper import expr

motion_trigger = []
entities = AUTO_MOTION_ENTITIES

# motion: motion detected
def on_motion_factory(entity):
  @time_active((f"range(sunset - {entities.get(entity)['sun_diff']}min, sunrise + {entities.get(entity)['sun_diff']}min)" if 'sun_diff' in entities.get(entity) else EXPR_TIME_RANGE_DAY))
  @state_trigger(expr(entity, "on"), state_check_now=True)
  def on_motion(var_name=None): 
    if var_name in entities and "on" in entities.get(var_name):
      scene.turn_on(entity_id=entities.get(var_name).get("on"))
  motion_trigger.append(on_motion) 

# motion: no motion detected
def off_motion_factory(entity):
  @state_trigger(expr(entity, "off"), state_hold=AUTO_MOTION_TIMEOUT, state_check_now=True)
  def off_motion(var_name=None):
    if var_name in entities and "off" in entities.get(var_name):
      transition = float(entities.get(var_name).get("transition")) if entities.get(var_name).get("transition") else 0
      scene.turn_on(entity_id=entities.get(var_name).get("off"), transition=float())
  motion_trigger.append(off_motion)

for entity in AUTO_MOTION_ENTITIES:
  on_motion_factory(entity)
  off_motion_factory(entity)