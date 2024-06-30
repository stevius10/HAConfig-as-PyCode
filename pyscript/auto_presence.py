from constants.mappings import STATE_ON, STATE_OFF, STATE_UNAVAILABLE, STATE_UNKNOWN

from utils import *

AUTO_PRESENCE_ENTITIES = {
  "wohnzimmer": {
    "indicators": {
      "media_player.wz_fernseher": {"condition": "playing"},
      "fan.wz_ventilator": {"condition": "playing", "weight": 0.1}
    },
    "exclusions": {
      "media_player.schlafzimmer": {"condition": "playing", "weight": 0.9},
    }
  },
  "schlafzimmer": {
    "indicators": {
      "media_player.sz_fernseher": {"condition": "playing"},
      "media_player.schlafzimmer": {"condition": "playing"},
      "fan.sz_ventilator": {"condition": "playing", "weight": 0.1}
    },
    "exclusions": {}
  },
  "away": {
    "indicators": {
      "person.steven": {"condition": "not_home"}
    },
    "exclusions": {}
  }
}

AUTO_PRESENCE_TRANSITION = {
  "wohnzimmer": {
    "on": [],
    "off": [
      {
        "condition": "state.get('climate.wohnzimmer') 'on'",
        "action": lambda: service.call("climate", "set_temperature", entity_id="climate.wohnzimmer", temperature=18)
      },
      {
        "condition": "state.get('light.wz_beleuchtung') 'on'",
        "action": lambda: service.call("light", "turn_off", entity_id="light.wz_beleuchtung")
      }
    ]
  },
  "schlafzimmer": {
    "on": [],
    "off": [
      {
        "condition": "state.get('climate.schlafzimmer') 'on'",
        "action": lambda: service.call("climate", "set_temperature", entity_id="climate.schlafzimmer", temperature=18)
      },
      {
        "condition": "state.get('light.sz_beleuchtung') 'on'",
        "action": lambda: service.call("light", "turn_off", entity_id="light.sz_beleuchtung")
      }
    ]
  },
  "away": {
    "on": [
      {
        "condition": "state.get('climate.wohnzimmer') 'on' or state.get('climate.schlafzimmer') 'on'",
        "action": lambda: [
          service.call("climate", "turn_off", entity_id="climate.schlafzimmer")
        ]
      },
      {
        "condition": "state.get('light.wz_beleuchtung') 'on' or state.get('light.sz_beleuchtung') 'on'",
        "action": lambda: [
          service.call("light", "turn_off", entity_id="light.wz_beleuchtung"),
          service.call("light", "turn_off", entity_id="light.sz_beleuchtung")
        ]
      }
    ],
    "off": []
  }
}

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
  if current_state is None or current_state in [STATE_UNAVAILABLE, STATE_UNKNOWN]:
    return False
  return eval(f"'{current_state}' {state}")

def weight(room, category):
  return sum([item.get('weight', 1) for item in AUTO_PRESENCE_ENTITIES[room][category].values() if evaluate(item['condition'])])

# Initialization
for room in AUTO_PRESENCE_ENTITIES:
  presence_factory(room, 'on')
  presence_factory(room, 'off')