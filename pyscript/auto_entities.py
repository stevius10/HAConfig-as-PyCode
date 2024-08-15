import regex as re
from constants.entities import ENTITIES_AUTO
from constants.mappings import MAP_EVENT_SYSTEM_STARTED, MAP_SERVICE_HA_TURNOFF, MAP_STATE_HA_TIMER_ACTIVE
from generic import RESULT_STATUS
from utils import *

trigger = []

entities = ENTITIES_AUTO

def default_factory(entity, default, call=MAP_SERVICE_HA_TURNOFF, params={}, delay=0, duration=0):
  is_default, is_not_default = [(expr(entity, default, compare, previous=True) if isinstance(default, (str, list)) else default) for compare in ('==', '!=')]

  entity_name = entity.split(".")[1]
  entity_timer = f"timer.{entity_name}"

  def default_call(call=call): 
    return service.call(call.split(".")[0], call.split(".")[1], **{**params, 'entity_id': entity})

  @state_trigger(is_not_default, state_hold_false=0)
  @task_unique(entity)
  @debugged
  def default_timer(delay=delay):
    if delay > 0:
      timer.start(entity_id=entity_timer, duration=delay)
      return resulted(RESULT_STATUS.STARTED, entity=entity_timer, duration=delay)
    else:
      return default_call()

  if delay > 0:
    @event_trigger("timer.finished", f"entity_id == '{entity_timer}'")
    @state_trigger(is_default, state_hold=duration)
    @task_unique(entity)
    @debugged
    def default_reset(**kwargs):
      timer.cancel(entity_id=entity_timer)
      return resulted(RESULT_STATUS.STOPPED, entity=entity_timer, details=default_call())

    trigger.extend([default_reset])
  trigger.extend([default_timer])

for entity, details in entities.items():
  default_factory(entity, details.get("default"),
    **{k: v for k, v in details.items() if k in {"call", "params", "delay", "duration"}})
