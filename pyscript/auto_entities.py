import regex as re
from constants.entities import ENTITIES_AUTO
from constants.mappings import MAP_SERVICE_HA_TURNOFF, MAP_STATE_HA_TIMER_ACTIVE
from generic import RESULT_STATUS
from utils import *

trigger = []

entities = ENTITIES_AUTO

def reset_factory(entity, default, call=MAP_SERVICE_HA_TURNOFF, params={}, delay=0, duration=0):
  is_not_default = expr(entity, default, '!=') if isinstance(default, (str, list)) else default
  
  entity_name = entity.split(".")[1]
  entity_timer = f"timer.{entity_name}"

  @logged
  def reset():
    return service.call(call.split(".")[0], call.split(".")[1], **{**params, 'entity_id': entity})

  @state_trigger(is_not_default, state_hold_false=0)
  @debugged
  def reset_start():
    if delay > 0:
      timer.start(entity_id=entity_timer, duration=delay)
      return resulted(RESULT_STATUS.STARTED, entity=entity_timer, duration=delay)
    else:
      return reset()

  if delay > 0:
    @event_trigger("timer.finished", f"entity_id == '{entity_timer}'")
    @state_active(expr(entity_timer, MAP_STATE_HA_TIMER_ACTIVE))
    @debugged
    def reset_timer_stop(**kwargs):
      timer.stop(entity_id=entity_timer)
      return resulted(RESULT_STATUS.STOPPED, entity=entity_timer, details=reset())

    @state_trigger(f"not ({is_not_default})", state_check_now=False, state_hold=duration)
    @state_active(expr(entity_timer, MAP_STATE_HA_TIMER_ACTIVE))
    @debugged
    def reset_timer_reset(var_name=None, value=None, old_value=None):
      timer.cancel(entity_id=entity_timer)
      return resulted(RESULT_STATUS.CANCELED, entity=entity_timer, state=value)
    trigger.extend([reset_timer_stop, reset_timer_reset])
  trigger.extend([reset_start])

for entity, details in entities.items():
  reset_factory(entity, details.get("default"),
    **{k: v for k, v in details.items() if k in {"call", "params", "delay", "duration"}})
