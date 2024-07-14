from constants.entities import ENTITIES_CONTROL
from constants.settings import SET_CONTROL_ON_LONG_HOLD

from utils import *

trigger = []

def on_press_factory(entity): 
  @state_trigger(expr(entity, expression=['on-press', 'off-press', 'up-press', 'down-press', 'single-press', 'double-press', 'long-press'], comparator="in", defined=False))
  @debugged
  def on_press(var_name=None, value=None):
    action = ENTITIES_CONTROL.get(entity).get(value.split("-")[0])
    if action:
      scene.turn_on(entity_id=action)
  trigger.append(on_press)

  @state_trigger(expr(entity, expression=['on-press'], comparator="in", defined=False), state_hold=SET_CONTROL_ON_LONG_HOLD)
  @debugged
  def on_long_press(var_name=None, value=None):
    action_on = ENTITIES_CONTROL.get(entity).get('on')
    action_off = ENTITIES_CONTROL.get(entity).get('on_long')
    if action_on:
      scene.turn_on(entity_id=action_on)
      task.sleep(ENTITIES_CONTROL.get(entity).get('on_long').get("duration"))
      scene.turn_off(entity_id=action_off)
  trigger.append(on_long_press)

for entity in ENTITIES_CONTROL:
  on_press_factory(entity)
