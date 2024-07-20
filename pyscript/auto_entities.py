import re

from constants.entities import ENTITIES_AUTO
from constants.mappings import MAP_EVENT_SYSTEM_STARTED, MAP_PERSISTENCE_PREFIX_TIMER, MAP_SERVICE_HA_TURNOFF, MAP_STATE_HA_TIMER_IDLE
from constants.settings import SET_ENTITIES_GLOBAL_VOLUME_MAX

from utils import *

trigger = []

entities = ENTITIES_AUTO

# Default 

def default_factory(entity, default, call, params):
  @state_trigger(f"{entity} {'!=' if isinstance(default, str) else 'not in'} {repr(default)} and {expr(entity, '', defined=True)}")
  def default():
    params = ", ".join(f"{k}={v}" for k, v in params.items())
    eval(f"service.call('{call.split('.')[0]}', '{call.split('.')[1]}', {params})")

def timeout_factory(entity, default, delay=0): # consider delay set 0 to replace default factory
  entity_name = entity.split(".")[1]
  entity_timer = f"timer.{entity_name}"
  entity_persisted = f"pyscript.{MAP_PERSISTENCE_PREFIX_TIMER}_{entity_name}"

  @event_trigger(MAP_EVENT_SYSTEM_STARTED)
  @debugged
  def timer_init():
    remaining = store(entity=entity_persisted, default=MAP_STATE_HA_TIMER_IDLE)
    if remaining and re.match(r'^\d{2}:\d{2}(:\d{2}(\.\d{1,3})?)?$', remaining):
      timer_start(delay=remaining)
      result_timer_init = f"[{entity_timer}] restored with duration {duration}"
    store(entity=entity_persisted, value="")
  @time_trigger('shutdown')

  @state_trigger(f"{entity} {'!=' if isinstance(entities.get(entity, {}).get('default'), str) else 'not in'} {repr(entities.get(entity, {}).get('default'))} and {expr(entity, '', defined=True)}", state_hold=1)
  @debugged
  def timer_start(duration=delay, trigger_type=None, var_name=None):
    entity_state = state.get(entity)
    if entity_state is not None and entity_state != entities.get(entity, {}).get('default') and entity_state not in MAP_STATE_HA_UNDEFINED:
      timer.start(entity_id=entity_timer, duration=duration)

  @event_trigger("timer.finished", f"entity_id == '{entity_timer}'")
  @debugged
  def timer_stop(**kwargs):
    service.call("homeassistant", f"turn_{default[0] if isinstance(default, list) else default}", entity_id=entity)

  @state_trigger(expr(entity, entities.get(entity)['default']), state_hold=1)
  @debugged
  def timer_reset():
    timer.cancel(entity_id=entity)

  @time_trigger('shutdown')
  def timer_shutdown():
    if entity_persisted is not None and state.get(entity_timer) and state.get(entity_timer) is not MAP_STATE_HA_TIMER_IDLE:
      timer.pause(entity_id=entity_timer) 
      homeassistant.update_entity(entity_id=entity_timer)
      store(entity=entity_persisted, value=state.getattr(entity_timer).get('remaining'))

  trigger.append(timer_init)
  trigger.append(timer_start)
  trigger.append(timer_stop)
  trigger.append(timer_reset)
  trigger.append(timer_shutdown)

for entity in entities:
  if "delay" not in entities[entity]:
    if "expr" not in entities[entity]:
      entities[entity]["expr"] = MAP_SERVICE_HA_TURNOFF
    default_factory(entity, entities.get(entity)['default'], entities.get(entity)['call'], entities.get(entity)['params'])
  else: 
    timeout_factory(entity, entities[entity]["default"], entities[entity]["delay"])