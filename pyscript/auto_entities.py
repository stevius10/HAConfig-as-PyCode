import re

from constants.entities import ENTITIES_AUTO
from constants.mappings import MAP_EVENT_SYSTEM_STARTED, MAP_PERSISTENCE_PREFIX_TIMER, MAP_SERVICE_HA_TURNOFF, MAP_STATE_HA_TIMER_IDLE, MAP_STATE_HA_UNDEFINED
from constants.settings import SET_ENTITIES_GLOBAL_VOLUME_MAX

from utils import *

trigger = []

entities = ENTITIES_AUTO

# Default 

def default_factory(entity, default, call, params):
  call_service = call.split(".")
  @state_trigger(f"{entity} {'!=' if isinstance(default, str) else 'not in'} {repr(default)} and {entity} != None")
  def default_action():
    parameters = ", ".join(f"{k}={v}" for k, v in params.items())
    service.call(call_service[0], call_service[1], parameters)

def timeout_factory(entity, default, delay=0): # consider delay set 0 to replace default factory
  entity_name = entity.split(".")[1]
  entity_timer = f"timer.{entity_name}"
  entity_persisted = f"pyscript.{MAP_PERSISTENCE_PREFIX_TIMER}_{entity_name}"

  @event_trigger(MAP_EVENT_SYSTEM_STARTED)
  @logged
  def timer_init():
    remaining = store(entity=entity_persisted, default=MAP_STATE_HA_TIMER_IDLE)
    if remaining and re.match(r'[0-9]{1,2}:[0-5][0-9]:[0-5][0-9]', remaining):
      timer_start(duration=remaining)
    else:
      timer_start()
    store(entity=entity_persisted, value=MAP_STATE_HA_TIMER_IDLE)
    if remaining and remaining != MAP_STATE_HA_TIMER_IDLE:
      return {"entity": entity_timer, "status": "restored", "details": {"duration": remaining}}

  @state_trigger(expr(entity, default, "!=", defined=False), state_hold=1)
  @debugged
  def timer_start(duration=delay):
    entity_state = state.get(entity)
    if entity_state is not None and (entity_state != default or entity_state not in default) and entity_state not in MAP_STATE_HA_UNDEFINED:
      service.call("timer", "start", entity_id=entity_timer, duration=duration)
      return {"entity": entity_timer, "status": "started", "details": {"duration": duration}}

  @event_trigger("timer.finished", f"entity_id == '{entity_timer}'")
  @debugged
  def timer_stop(**kwargs):
    service.call("homeassistant", f"turn_{default[0] if isinstance(default, list) else default}", entity_id=entity)
    return {"entity": entity_timer, "status": "stopped", "details": kwargs}

  @state_trigger(expr(entity, default, defined=False), state_hold=1)
  @debugged
  def timer_reset(var_name=None, value=None):
    service.call("timer", "cancel", entity_id=entity_timer)
    return {"entity": entity_timer, "status": "canceled", "details": {"entity": var_name, "state": value}}

  @time_trigger('shutdown')
  def timer_shutdown():
    if state.get(entity_timer) and state.get(entity_timer) != MAP_STATE_HA_TIMER_IDLE:
      service.call("timer", "pause", entity_id=entity_timer)
      remaining = state.getattr(entity_timer).get('remaining')
      store(entity=entity_persisted, value=remaining, result=False)
      return {"entity": entity_timer, "status": "stored", "details": {"remaining": remaining}}

  trigger.extend([timer_init, timer_start, timer_stop, timer_reset, timer_shutdown])

for entity in entities:
  if "delay" not in entities[entity]:
    if "expr" not in entities[entity]:
      entities[entity]["expr"] = MAP_SERVICE_HA_TURNOFF
    default_factory(entity, entities[entity]['default'], entities[entity]['call'], entities[entity]['params'])
  else:
    timeout_factory(entity, entities[entity]["default"], entities[entity]["delay"])