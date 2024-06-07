from constants.entities import CONFIG_CONTROL_ENTITIES
from utils import expr

trigger = []

def on_press_factory(entity): 

  @state_trigger(expr(entity, expression=['on-press', 'off-press', 'up-press', 'down-press', 'single-press', 'double-press', 'long-press'], comparator="in", defined=False))
  def on_press(var_name=None, value=None):
    action = CONFIG_CONTROL_ENTITIES.get(entity).get(value.split("-")[0])
    scene.turn_on(entity_id=action)
  trigger.append(on_press)

for entity in CONFIG_CONTROL_ENTITIES:
  on_press_factory(entity)


# Higher computational complexity in favor of readability
#
# from utils import *
#
# entities = CONFIG_CONTROL
#
# trigger_control = []
#
# def on_press_factory(entity): 
#
#   @state_trigger(expr(entity, expression=['on-press', 'off-press', 'up-press', 'down-press', 'single-press', 'double-press', 'long-press'], comparator="in", defined=True, logs=False))
#   def on_press(var_name=None, value=None):
#     action = entities.get(entity).get(value.split("-")[0])
#     if action is not None: 
#       if isinstance(action, list):
#         for item in action:
#           turn_on(item)
#       if isinstance(action, str): 
#         turn_on(action)
#   trigger_control.append(on_press)

# for entity in entities:
#   on_press_factory(entity)
#
# def turn_on(entity):
#   if isinstance(entity, list): 
#     for e in entity: 
#       turn_on(e)
#   elif isinstance(entity, (str)): 
#     homeassistant.turn_on(entity_id=entity)