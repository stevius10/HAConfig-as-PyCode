from constants.data import DATA_PRESENCE
from constants.entities import ENTITIES_PRESENCE
from constants.mappings import PERSISTENCE_ENTITY_AUTO_PRESENCE
from utils import *

trigger = []

def presence_factory(room, action):
  
  @time_trigger('startup')
  def presence_init(): 
    state.persist(PERSISTENCE_ENTITY_AUTO_PRESENCE)
    homeassistant.update_entity(entity_id=entity)

  @state_trigger([expr(entity, str(condition.get('condition'))) for entity, condition in ENTITIES_PRESENCE.get(room).get('indicators').items()], state_hold=ENTITIES_PRESENCE.get(room).get('indicators').get('duration'))
  @logged
  def presence(var_name=None):
    indicator_weight = weight(room, 'indicators')
    exclusion_weight = weight(room, 'exclusions')
    if indicator_weight >= 1 and exclusion_weight == 0:
      persist(room, 'on')
      transition(room, 'on')
    elif indicator_weight < 1 or exclusion_weight > 0:
      persist(room, 'off')
      transition(room, 'off')
  trigger.append(presence)

def persist(room, action):
  state.set(PERSISTENCE_ENTITY_AUTO_PRESENCE, "'{}'".format(str(state.get(f"{PERSISTENCE_ENTITY_AUTO_PRESENCE}.wohnzimmer") == "on") or \
      str(state.get(f"'{PERSISTENCE_ENTITY_AUTO_PRESENCE}.schlafzimmer'") == "on")), attributes={room: action})
  homeassistant.update_entity(entity_id=PERSISTENCE_ENTITY_AUTO_PRESENCE)
  state.persist(PERSISTENCE_ENTITY_AUTO_PRESENCE)

def weight(room, category):
  return 0 # sum([item.get('weight', 1) for item in ENTITIES_PRESENCE[room][category].values()]) # TODO: if eval(item['condition'])])
  
def transition(room, action):
  for transition in DATA_PRESENCE.get(room, {}).get(action, []):
    if eval(transition['condition']):
      transition['action']()
      
# Initialization

for room in ENTITIES_PRESENCE:
  presence_factory(room, 'on')
  presence_factory(room, 'off')