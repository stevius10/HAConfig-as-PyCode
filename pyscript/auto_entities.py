import regex as re

from constants.entities import ENTITIES_AUTO
from constants.mappings import MAP_EVENT_SYSTEM_STARTED, MAP_PERSISTENCE_PREFIX_TIMER, MAP_SERVICE_HA_TURNOFF, MAP_STATE_UNDEFINED
from constants.settings import SET_ENTITIES_GLOBAL_VOLUME_MAX

from utils import *

trigger = []

entities = ENTITIES_AUTO

def default_factory(entity, default, call, params):
  call_service = call.split(".")
  @state_trigger(f"{entity} {'!=' if isinstance(default, str) else 'not in'} {repr(default)} and {entity} != None")
  def default_action():
    parameters = {k: v for k, v in params.items()}
    service.call(call_service[0], call_service[1], **parameters)

def timeout_factory(entity, default, delay=0):
  entity_name = entity.split(".")[1]
  entity_timer = f"timer.{entity_name}"
  entity_persisted = f"pyscript.{MAP_PERSISTENCE_PREFIX_TIMER}_{entity_name}"

  @event_trigger(MAP_EVENT_SYSTEM_STARTED)
  @logged
  def timer_init():
    remaining = store(entity=entity_persisted)
    if remaining and re.match(r'[0-9]{1,2}:[0-5][0-9]:[0-5][0-9]', str(remaining)):
      timer_start(duration=remaining)
      store(entity=entity_persisted, value="")
      return {"entity": entity_timer, "status": "restored", "details": {"duration": remaining}}
    else:
      homeassistant.update_entity(entity_id=entity)

  @state_trigger(f"{entity} != {repr(default)}", state_hold=1)
  @debugged
  def timer_start(duration=delay):
    timer.start(entity_id=entity_timer, duration=delay)
    return {"entity": entity_timer, "status": "started", "details": {"duration": duration}}

  @event_trigger("timer.finished", f"entity_id == '{entity_timer}'")
  @debugged
  def timer_stop(**kwargs):
    service.call("homeassistant", f"turn_{default[0] if isinstance(default, list) else default}", entity_id=entity)
    store(entity=entity_persisted, value="")
    return {"entity": entity_timer, "status": "stopped", "details": kwargs}

  @state_trigger(f"{entity} == {repr(default)}", state_check_now=False, state_hold_false=0, state_hold=1)
  @debugged
  def timer_reset(var_name=None, value=None, old_value=None):
    if old_value not in MAP_STATE_UNDEFINED:
      service.call("timer", "cancel", entity_id=entity_timer)
      store(entity=entity_persisted, value="")
      return {"entity": entity_timer, "status": "canceled", "details": {"entity": var_name, "state": value}}

  @time_trigger('shutdown')
  def timer_shutdown():
    service.call("timer", "pause", entity_id=entity_timer, blocking=True)
    homeassistant.update_entity(entity_id=entity_timer)
    store(entity=entity_persisted, value=state.getattr(entity_timer).get('remaining', ''), result=False)

  trigger.extend([timer_init, timer_start, timer_stop, timer_reset, timer_shutdown])

for entity in entities:
  if "delay" not in entities[entity]:
    if "expr" not in entities[entity]:
      entities[entity]["expr"] = MAP_SERVICE_HA_TURNOFF
    default_factory(entity, entities[entity]['default'], entities[entity]['call'], entities[entity]['params'])
  else:
    timeout_factory(entity, entities[entity]["default"], entities[entity]["delay"])
