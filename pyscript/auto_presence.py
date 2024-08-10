from constants.data import DATA_PRESENCE
from constants.entities import ENTITIES_PRESENCE
from constants.mappings import MAP_EVENT_SYSTEM_STARTED, MAP_PERSISTENCE_ENTITY_PRESENCE

from utils import *

trigger = []

def presence_factory(room):

  @event_trigger(MAP_EVENT_SYSTEM_STARTED)
  def presence_init():
    store(MAP_PERSISTENCE_ENTITY_PRESENCE)

  trigger_conditions = [expr(entity, condition['condition']) for entity, condition in ENTITIES_PRESENCE[room]['indicators'].items()]
  # @state_trigger(trigger_conditions)
  @logged
  def presence(var_name=None):
    indicators_weight = sum([condition.get('weight', 1) for entity, condition in ENTITIES_PRESENCE[room]['indicators'].items() if state.get(entity) == condition['condition']])
    exclusions_weight = sum([condition.get('weight', 1) for entity, condition in ENTITIES_PRESENCE[room]['exclusions'].items() if state.get(entity) == condition['condition']])
    if indicators_weight >= 1 and exclusions_weight == 0:
      update_presence(room, 'on')
    else:
      update_presence(room, 'off')
  trigger.append(presence)

def update_presence(room, action, entity=MAP_PERSISTENCE_ENTITY_PRESENCE):
  if entity: 
    current_state = state.get(entity) if state.get(entity) else {}
    attributes = current_state.get('attributes', {}) if current_state else {}
    attributes[room] = action
    global_state = 'on' if any(status == 'on' for status in attributes.values()) else 'off'
    store(entity, global_state, attributes=attributes)

  for transition in DATA_PRESENCE.get(room, {}).get(action, []):
    if eval(transition['condition']):
      transition['action']()

for room in ENTITIES_PRESENCE:
  presence_factory(room)
