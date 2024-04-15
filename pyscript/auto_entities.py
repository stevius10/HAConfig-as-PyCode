from entities import AUTO_ENTITIES_DEFAULT, AUTO_TIMEOUT_ENTITIES
from helper import expr
from utils import log

from homeassistant.const import EVENT_HOMEASSISTANT_STARTED

entities_default = AUTO_ENTITIES_DEFAULT
entities_timeout = AUTO_TIMEOUT_ENTITIES

default_trigger = []
timeout_trigger = []

ha_service_turn_off = "homeassistant.turn_off"

# Default 

def default_factory(entity, func):
  @state_trigger(expr(entity, entities_default.get(entity)['default'], comparator="!="), func)
  def default(func):
    service.call(func.split(".")[0], func.split(".")[1], entity_id=entity)
  default_trigger.append(default)

# Timeout

def timeout_factory(entity, default, delay=None):
  @event_trigger(EVENT_HOMEASSISTANT_STARTED) 
  @state_trigger(expr(entity, expression=entities_timeout.get(entity)['default'], comparator="!=", defined=True))
  def timeout_default(trigger_type=None, var_name=None):
    if state.get(entity) != default:
      if trigger_type == "event" or delay == None: 
        reset(entity, default)
      if delay in entities_timeout.get(entity): 
        entity_timer = get_timer(entity, delay)
        log(f"implement: kwargs: {entity_timer}")
        timer.cancel(entity_id=entity_timer)
        timer.start(entity_id=entity_timer, duration=delay)
  timeout_trigger.append(timeout_default)

  @event_trigger("timer.finished")
  def timer_stop(**kwargs):
    log(f"implement: kwargs: {kwargs}")
    reset(entity_id=entity)
  timeout_trigger.append(timer_stop)

# Initialization

for entity in entities_default:
  if "delay" not in entities_default[entity]:
    if "func" not in entities_default[entity]:
      entities_default[entity]["func"] = ha_service_turn_off
    default_factory(entity, entities_default.get(entity)['func'])
    
for entity in entities_timeout:
  timeout_factory(entity, entities_timeout[entity]["default"], entities_timeout[entity]["delay"])

# Helper

def reset(entity, default):
  if default in ["off"]:
    homeassistant.turn_off(entity_id=entity)
  elif default == "on":
    homeassistant.turn_on(entity_id=entity)
  state.set(entity, default)

def get_timer(entity, delay):
  return f"timer.timer_{entity.split(".")[1]}"