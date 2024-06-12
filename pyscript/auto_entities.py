from constants.entities import AUTO_ENTITIES
from constants.events import EVENT_SYSTEM_STARTED
from constants.mappings import SERVICE_HA_TURN_OFF

from utils import *

entities = AUTO_ENTITIES

trigger = []

# Default 

def default_factory(entity, func):
  @state_trigger(expr(entity, entities.get(entity)['default'], comparator="!="), func)
  @debugged
  def default(func):
    service.call(func.split(".")[0], func.split(".")[1], entity_id=entity)
  trigger.append(default)

# Timeout

def timeout_factory(entity, default, delay=0):
  
  entity_name = entity.split(".")[1]
  entity_timer = f"timer.{entity_name}"
  entity_persistence = f"pyscript.{entity_name}"
  state.persist(entity_persistence)
  
  @event_trigger(EVENT_SYSTEM_STARTED)
  @state_trigger(expr(entity, expression=default, comparator="!=", defined=True), state_check_now=True)
  @debugged
  def start_timer(delay=delay, trigger_type=None, var_name=None):
    if state.get(entity) != default and state.get(entity) not in STATES_UNDEFINED:
      if trigger_type == "event": 
        persisted = state.get(entity_persistence)
        if persisted: delay = persisted
      elif "delay" in entities.get(entity): 
        timer.cancel(entity_id=entity_timer)
      timer.start(entity_id=entity_timer, duration=delay)
  trigger.append(start_timer)

  @event_trigger("timer.finished", f"entity_id == '{entity_timer}'")
  @debugged
  def timer_stop(**kwargs):
    service.call("homeassistant", f"turn_{default}", entity_id=entity)
  trigger.append(timer_stop)
  
  @state_trigger(expr(entity, expression=default, comparator="=="))
  @debugged
  def timer_reset(var_name=None):
    timer.cancel(entity_id=entity_timer)
  trigger.append(timer_reset)
  
  @time_trigger("shutdown")
  def timer_persist():
    entity_timer_state = state.get(entity_timer)
    if entity_timer_state and entity_timer_state is not "idle":
      state.set(entity_persistence, state.get(f"{entity_timer}.duration"))

# Initialization

for entity in entities:
  if "delay" not in entities[entity]:
    if "func" not in entities[entity]:
      entities_default[entity]["func"] = SERVICE_HA_TURN_OFF
    default_factory(entity, entities.get(entity)['func'])
  else: 
    timeout_factory(entity, entities[entity]["default"], entities[entity]["delay"])