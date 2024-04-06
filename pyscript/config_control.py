from helper import expr
from utils import Logs

CONFIG_CONTROL = {
  'sensor.wz_schalter_action': {
    'on': 'scene.wz_indirekt',
    'off': 'scene.wz_aus',
    'up': 'scene.wz_hell',
    'down': 'scene.wz_schwach'
  }, 
  'sensor.sz_schalter_action': {
    'on': 'scene.sz_indirekt',
    'off': 'scene.sz_aus',
    'up': 'scene.sz_hell',
    'down': 'scene.sz_schwach'
  },
  'sensor.g_schalter_action': {
    'single': 'scene.g_indirekt',
    'double': 'scene.g_aus',
    'long': 'scene.g_wz_k_g'
  }
}

trigger_control = []

def on_press_factory(entity): 
  
  @state_trigger(expr(entity, defined=True))
  def on_press(var_name=None, value=None):
    try:
      action = CONFIG_CONTROL.get(entity).get(value.split("-")[0])
      if action:
        Logs(action)
        scene.turn_on(entity_id=action)
    except KeyError:
      Logs()

  trigger_control.append(on_press)

for entity in CONFIG_CONTROL:
  on_press_factory(entity)