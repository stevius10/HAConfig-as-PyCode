from entities import AUTO_ENTITIES
from mapping import SERVICE_HA_TURN_OFF
from utils import *

from homeassistant.const import EVENT_HOMEASSISTANT_STARTED

entities = AUTO_ENTITIES

trigger = []

# Default 

def default_factory(entity, func):
  @state_trigger(expr(entity, entities.get(entity)['default'], comparator="!="), func)
  def default(func):
    service.call(func.split(".")[0], func.split(".")[1], entity_id=entity)
  trigger.append(default)

# Timeout

def timeout_factory(entity, default, delay=None):
  
  entity.split(".")[0]
  entity_name = entity.split(".")[1]
  entity_timer = f"timer.{entity_name}"
  
  @event_trigger(EVENT_HOMEASSISTANT_STARTED)
  @state_trigger(expr(entity, expression=default, comparator="!=", defined=True))
  def start_timer(trigger_type=None, var_name=None):
    if state.get(entity) != default:
      if trigger_type == "event" or delay == None: 
        timer_stop(entity=entity)
      if "delay" in entities.get(entity): 
        timer.cancel(entity_id=entity_timer)
        timer.start(entity_id=entity_timer, duration=delay)
  trigger.append(start_timer)

  @event_trigger("timer.finished", f"entity_id == '{entity_timer}'")
  def timer_stop(**kwargs):
    service.call("homeassistant", f"turn_{default}", entity_id=entity)
  trigger.append(timer_stop)
  
  @state_trigger(expr(entity, expression=default, comparator="=="))
  def timer_reset(var_name=None):
    timer.cancel(entity_id=entity_timer)
  trigger.append(timer_reset)

# Initialization

for entity in entities:
  if "delay" not in entities[entity]:
    if "func" not in entities[entity]:
      entities_default[entity]["func"] = SERVICE_HA_TURN_OFF
    default_factory(entity, entities.get(entity)['func'])
  else: 
    timeout_factory(entity, entities[entity]["default"], entities[entity]["delay"])