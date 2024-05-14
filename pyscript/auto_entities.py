from entities import AUTO_ENTITIES
from utils import *

from homeassistant.const import EVENT_HOMEASSISTANT_STARTED

entities = AUTO_ENTITIES

default_trigger = []
timeout_trigger = []

ha_service_turn_off = "homeassistant.turn_off"

# Default 

def default_factory(entity, func):
  @state_trigger(expr(entity, entities.get(entity)['default'], comparator="!="), func)
  def default(func):
    service.call(func.split(".")[0], func.split(".")[1], entity_id=entity)
  default_trigger.append(default)

# Timeout

def timeout_factory(entity, default, delay=None):
  
  @event_trigger(EVENT_HOMEASSISTANT_STARTED) 
  @state_trigger(expr(entity, expression=entities.get(entity)['default'], comparator="!=", defined=True))
  def timeout_start_timer(trigger_type=None, var_name=None):
    if state.get(entity) != default:
      if trigger_type == "event" or delay == None: 
        reset(entity, default)
      if "delay" in entities.get(entity): 
        entity_timer = f"timer.{entity.split(".")[1]}"
        timer.cancel(entity_id=entity_timer)
        timer.start(entity_id=entity_timer, duration=delay)
  timeout_trigger.append(timeout_start_timer)

  @event_trigger("timer.finished", f"entity_id == 'timer.{entity.split(".")[1]}'")
  def timer_stop(**kwargs):
    reset(entity=entity, default=default)
  timeout_trigger.append(timer_stop)

  @state_trigger(expr(entity, expression=entities.get(entity)['default'], comparator="=="))
  def timer_reset(var_name=None):
    entity_timer = f"timer.{var_name.split(".")[1]}"
    timer.cancel(entity_id=entity_timer)
  timeout_trigger.append(timer_reset)

# Initialization

for entity in entities:
  if "delay" not in entities[entity]:
    if "func" not in entities[entity]:
      entities_default[entity]["func"] = ha_service_turn_off
    default_factory(entity, entities.get(entity)['func'])
  else: 
    timeout_factory(entity, entities[entity]["default"], entities[entity]["delay"])

# Helper

def reset(entity, default):
  if default == "off":
    homeassistant.turn_off(entity_id=entity)
  elif default == "on":
    homeassistant.turn_on(entity_id=entity)
  state.set(entity, default)
  
  # Initialization

for entity in entities:
  if "delay" not in entities[entity]:
    if "func" not in entities[entity]:
      entities_default[entity]["func"] = ha_service_turn_off

    default_factory(entity, entities.get(entity)['func'])
  else: 
    timeout_factory(entity, entities[entity]["default"], entities[entity]["delay"])