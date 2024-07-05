import re

from constants.entities import ENTITIES_AUTO
from constants.mappings import MAP_EVENT_SYSTEM_STARTED, PERSISTENCE_PREFIX_PREFIX, MAP_SERVICE_HA_TURNOFF
from utils import *

trigger = []

entities = ENTITIES_AUTO

# Default 

def default_factory(entity, func):
  @state_trigger(expr(entity, entities.get(entity)['default'], comparator="!="), func, state_hold=1)
  @debugged
  def default(func):
    service.call(func.split(".")[0], func.split(".")[1], entity_id=entity)
  trigger.append(default)

# Timeout

def timeout_factory(entity, default, delay=0):
  entity_name = entity.split(".")[1]
  entity_timer = f"timer.{entity_name}"
  entity_persisted = f"pyscript.{PERSISTENCE_PREFIX_PREFIX}_{entity_name}"

  @state_trigger(expr(entity, expression=default, comparator="!=", defined=True), state_hold_false=1)
  @debugged
  def start_timer(delay=delay, trigger_type=None, var_name=None):
    if state.get(entity) != default and state.get(entity) not in MAP_STATE_HA_UNDEFINED:
      timer.start(entity_id=entity_timer, duration=delay)
  trigger.append(start_timer)

  @event_trigger("timer.finished", f"entity_id == '{entity_timer}'")
  @logged
  def timer_stop(**kwargs):
    service.call("homeassistant", f"turn_{default[0] if isinstance(default, list) else default}", entity_id=entity)
  trigger.append(timer_stop)
  
  @state_trigger(expr(entity, expression=default, comparator="=="), state_hold=1)
  @debugged
  def timer_reset(var_name=None):
    timer.cancel(entity_id=entity_timer)
  trigger.append(timer_reset)

  # Handle system based events 

  @time_trigger('startup')
  def timer_init(): 
    state.persist(entity_persisted, "idle")
    homeassistant.update_entity(entity_id=entity_persisted)

  @event_trigger(MAP_EVENT_SYSTEM_STARTED)
  def timer_restore():
    if state.get(entity_persisted) and re.match(r'^\d{2}:\d{2}(:\d{2}(\.\d{1,3})?)?$', state.get(entity_persisted)): # 'HH:MM', 'HH:MM:SS', 'HH:MM:SS.F'
      start_timer(delay=str(state.get(entity_persisted)))
      log(f"timer '{entity_timer}' restored with duration {state.getattr(entity_timer).get('remaining')}")
    state.set(entity_persisted, "")

  @time_trigger('shutdown')
  def timer_persist():
    if entity_persisted and state.get(entity_timer):
      timer.pause(entity_id=entity_timer)
      homeassistant.update_entity(entity_id=entity_timer)
      state.set(entity_persisted, state.getattr(entity_timer).get('remaining'))
      homeassistant.update_entity(entity_id=entity_persisted)
      state.persist(entity_persisted)
          
# Initialization

for entity in entities:
  if "delay" not in entities[entity]:
    if "func" not in entities[entity]:
      entities_default[entity]["func"] = MAP_SERVICE_HA_TURNOFF
    default_factory(entity, entities.get(entity)['func'])
  else: 
    timeout_factory(entity, entities[entity]["default"], entities[entity]["delay"])
