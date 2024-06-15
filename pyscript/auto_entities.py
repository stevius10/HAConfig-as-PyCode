from constants.entities import AUTO_ENTITIES
from constants.events import EVENT_SYSTEM_STARTED
from constants.mappings import PERSISTANCE_GENERAL_TIMER_PREFIX, SERVICE_HA_TURN_OFF

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
  entity_persisted = f"pyscript.{PERSISTANCE_GENERAL_TIMER_PREFIX}_{entity_name}"

  @state_trigger(expr(entity, expression=default, comparator="!=", defined=True), state_check_now=True)
  def start_timer(delay=delay, trigger_type=None, var_name=None):
    if state.get(entity) != default and state.get(entity) not in STATES_UNDEFINED:
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

  # Handle system based events 

  @time_trigger('startup')
  def timer_init():
    default_value = "idle"
    state.persist(entity_persisted, default_value=default_value)
    if state.get(entity_persisted) is not default_value:
      start_timer(delay=state.get(entity_persisted))
      log(f"timer '{entity_timer}' restored with duration {state.getattr(entity_timer).get('remaining')}")
    state.set(entity_persisted, default_value)

  @time_trigger('shutdown')
  def timer_persist():
    if entity_persisted is not None and state.get(entity_timer) and state.get(entity_timer) is not "idle":
      timer.pause(entity_id=entity_timer)
      task.sleep(0.5)
      state.set(entity_persisted, state.getattr(entity_timer).get('remaining'))
      state.persist(entity_persisted)
          
# Initialization

for entity in entities:
  if "delay" not in entities[entity]:
    if "func" not in entities[entity]:
      entities_default[entity]["func"] = SERVICE_HA_TURN_OFF
    default_factory(entity, entities.get(entity)['func'])
  else: 
    timeout_factory(entity, entities[entity]["default"], entities[entity]["delay"])