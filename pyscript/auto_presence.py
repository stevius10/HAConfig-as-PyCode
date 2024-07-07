from constants.data import DATA_PRESENCE
from constants.entities import ENTITIES_PRESENCE
from constants.mappings import PERSISTENCE_ENTITY_AUTO_PRESENCE
from utils import *

trigger = []

def presence_factory(room):
  
  trigger_conditions = [f"state.{entity} == '{condition['condition']}'" for entity, condition in ENTITIES_PRESENCE[room]['indicators'].items()]
  @state_trigger(trigger_conditions)
  @logged
  def presence(var_name=None):
    indicators_weight = sum(condition.get('weight', 1) for entity, condition in ENTITIES_PRESENCE[room]['indicators'].items() if state.get(entity) == condition['condition'])
    exclusions_weight = sum(condition.get('weight', 1) for entity, condition in ENTITIES_PRESENCE[room]['exclusions'].items() if state.get(entity) == condition['condition'])
    if indicators_weight >= 1 and exclusions_weight == 0:
      update_presence(room, 'on')
    else:
      update_presence(room, 'off')
  trigger.append(presence)

  @time_trigger('startup')
  def presence_init():
    existing_attributes = state.get(f"{PERSISTENCE_ENTITY_AUTO_PRESENCE}", {}).get('attributes', {})
    initial_attributes = {room: existing_attributes.get(room, 'off') for room in ENTITIES_PRESENCE}
    state.persist(f"{PERSISTENCE_ENTITY_AUTO_PRESENCE}", default_value="", attributes=initial_attributes)
    homeassistant.update_entity(entity_id=PERSISTENCE_ENTITY_AUTO_PRESENCE)

def update_presence(room, action):
  current_state = state.get(f"{PERSISTENCE_ENTITY_AUTO_PRESENCE}", {})
  attributes = current_state.get('attributes', {}) if current_state else {}
  attributes[room] = action
  global_state = 'on' if any(status == 'on' for status in attributes.values()) else 'off'
  state.set(f"{PERSISTENCE_ENTITY_AUTO_PRESENCE}", global_state, attributes=attributes)
  homeassistant.update_entity(entity_id=PERSISTENCE_ENTITY_AUTO_PRESENCE)
  state.persist(f"{PERSISTENCE_ENTITY_AUTO_PRESENCE}")
  
  for transition in DATA_PRESENCE.get(room, {}).get(action, []):
    if eval(transition['condition']):
      transition['action']()

for room in ENTITIES_PRESENCE:
  presence_factory(room)
