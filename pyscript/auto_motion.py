from constants import AUTO_CONFIG_MOTION_SUNSET_DIFF, AUTO_CONFIG_MOTION_TIMEOUT, AUTO_CONFIG_MOTION_TRANSITION
from helper import expr

motion_trigger = []

entities = { 
  "binary_sensor.k_sensor_occupancy": { "on": "scene.k_normal", "off": "scene.k_aus", "transition": AUTO_CONFIG_MOTION_TRANSITION, "sunset_diff": AUTO_CONFIG_MOTION_SUNSET_DIFF }, 
  "binary_sensor.g_sensor_occupancy": { "on": "scene.g_tisch", "off": "scene.g_aus", "transition": 0 }
}

# motion: motion detected
def on_motion_factory(entity):
  @time_active((f"range(sunset - {entities.get(entity)['sunset_diff']}min, sunrise + {entities.get(entity)['sunset_diff']}min)" if 'sunset_diff' in entities.get(entity) else "range(00:00, 24:00)"))
  @state_trigger(expr(entity, "on"), state_check_now=True)
  def on_motion(var_name=None): 
    if var_name in entities and "on" in entities.get(var_name):
      scene.turn_on(entity_id=entities.get(var_name).get("on"))
  motion_trigger.append(on_motion) 

# motion: no motion detected
def off_motion_factory(entity):
  @state_trigger(expr(entity, "off"), state_hold=AUTO_CONFIG_MOTION_TIMEOUT, state_check_now=True)
  def off_motion(var_name=None):
    if var_name in entities and "off" in entities.get(var_name):
      scene.turn_on(entity_id=entities.get(var_name)["off"], transition=entities.get(var_name)["transition"])
  motion_trigger.append(off_motion)

for entity in entities:
  on_motion_factory(entity)
  off_motion_factory(entity)