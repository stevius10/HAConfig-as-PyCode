from helper import expr
from utils import *

CONFIG_CONTROL = {
  'sensor.wz_schalter_action': {
    'on': 'scene.wz_indirekt',
    'off': ['scene.wz_aus', 'scene.k_aus'],
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
    'long': ''
  }
}

entities = CONFIG_CONTROL

trigger_control = []

def on_press_factory(entity): 

  @state_trigger(expr(entity, expression=['on-press', 'off-press', 'up-press', 'down-press', 'single-press', 'double-press', 'long-press'], comparator="in", defined=True, logs=False))
  def on_press(var_name=None, value=None):
    action = entities.get(entity).get(value.split("-")[0])
    if action is not None: 
      if isinstance(action, list):
        for item in action:
          turn_on(item)
      if isinstance(action, str): 
        turn_on(action)
  trigger_control.append(on_press)

for entity in entities:
  on_press_factory(entity)
  
def turn_on(entity):
  if isinstance(entity, list): 
    for e in entity: 
      turn_on(e)
  elif isinstance(entity, (str)): 
    homeassistant.turn_on(entity_id=entity)
