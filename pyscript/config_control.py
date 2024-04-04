from helper import expr
from utils import Logs

CONFIG_CONTROL = {
  'sensor.wz_schalter_action': {
    'on': 'scene.wz_indirekt',
    'off': 'scene.wz_aus',
    'up': 'scene.wz_hell',
    'down': 'scene.wz_schwach'
  }
}

trigger_control = []

def on_press_factory(entity): 
  
  @state_trigger(expr(entity, "!= None"))
  def on_press(var_name=None, value=None):
    try:
      action = CONFIG_CONTROL.get(entity).get([value.split("-")[0]])
      log.info(action)
      if action:
        scene.activate(action)
    except KeyError:
      Logs()

  trigger_control.append(on_press)

for entity in CONFIG_CONTROL:
  on_press_factory(entity)