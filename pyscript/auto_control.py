from constants.entities import ENTITIES_CONTROL

from utils import *

trigger = []

def on_press_factory(entity): 
  @state_trigger(expr(entity, expression=['on-press', 'off-press', 'up-press', 'down-press', 'single-press', 'double-press', 'long-press'], comparator="in", defined=False))
  @debugged
  def on_press(var_name=None, value=None):
    action = ENTITIES_CONTROL.get(entity).get(value.split("-")[0])
    scene.turn_on(entity_id=action)
  trigger.append(on_press)

for entity in ENTITIES_CONTROL:
  on_press_factory(entity)
