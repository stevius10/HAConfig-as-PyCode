from constants.entities import AUTO_PRESENCE_ENTITIES
from constants.settings import AUTO_PRESENCE_TRANSITION

from utils import *

trigger = []

def presence_factory(room, action):
  # TODO: @state_trigger([expr(entity, condition.get('condition')) for entity, condition in AUTO_PRESENCE_ENTITIES.get(room).get('indicators').items()], state_hold=AUTO_PRESENCE_ENTITIES.get(room).get('indicators').get('duration'))
  @logged
  def presence(var_name=None):
    indicator_weight = weight(room, 'indicators')
    exclusion_weight = weight(room, 'exclusions')
    if action == 'on' and indicator_weight >= 1 and exclusion_weight == 0:
      for other in AUTO_PRESENCE_ENTITIES:
        if other != room and other != 'away':
          deactivate(other)
      transition(room, 'on')
    elif action == 'off' and (indicator_weight < 1 or exclusion_weight > 0):
      transition(room, 'off')
  trigger.append(presence)

def transition(room, action):
  for transition in AUTO_PRESENCE_TRANSITION.get(room, {}).get(action, []):
    if eval(transition['condition']):
      transition['action']()

def evaluate(condition):
  entity, state = condition.split(' ', 1)
  current_state = state.get(entity)
  if current_state is None or current_state in STATES_HA_UNDEFINED:
    return False
  return eval(f"'{current_state}' {state}")

def weight(room, category):
  return sum([item.get('weight', 1) for item in AUTO_PRESENCE_ENTITIES[room][category].values() if evaluate(item['condition'])])

# Initialization
for room in AUTO_PRESENCE_ENTITIES:
  presence_factory(room, 'on')
  presence_factory(room, 'off')