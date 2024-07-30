import regex as re
from constants.entities import ENTITIES_AUTO
from constants.mappings import MAP_SERVICE_HA_TURNOFF, MAP_STATE_HA_TIMER_ACTIVE
from generic import RESULT_STATUS
from utils import *

trigger = []

entities = ENTITIES_AUTO

def reset_factory(entity, default, call=None, params={}, delay=0, duration=0):
  entity_name = entity.split(".")[1]
  entity_timer = f"timer.{entity_name}"
  call = call or MAP_SERVICE_HA_TURNOFF

  @logged
  def reset():
    return service.call(call.split(".")[0], call.split(".")[1], entity_id=entity, **params)

  is_not_default = expr(entity, default, '!=') if isinstance(default, (str, list)) else default

  @state_trigger(is_not_default, state_check_now=True)
  @debugged
  def reset_start():
    if delay > 0:
      timer.start(entity_id=entity_timer, duration=delay)
      return resulted(RESULT_STATUS.STARTED, entity=entity_timer, duration=delay)
    else:
      reset()

  if delay > 0:
    @event_trigger("timer.finished", f"entity_id == '{entity_timer}'")
    @state_active(expr(entity_timer, MAP_STATE_HA_TIMER_ACTIVE))
    @debugged
    def reset_timer_stop(**kwargs):
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


# import regex as re

# from constants.entities import ENTITIES_AUTO
# from constants.mappings import MAP_EVENT_SYSTEM_STARTED, MAP_PERSISTENCE_PREFIX_TIMER, MAP_STATE_HA_TIMER_ACTIVE, MAP_STATE_HA_TIMER_IDLE, MAP_SERVICE_HA_TURNOFF, MAP_STATE_HA_UNDEFINED
# from constants.settings import SET_ENTITIES_GLOBAL_VOLUME_MAX

# from generic import RESULT_STATUS
# from utils import *

# trigger = []

# entities = ENTITIES_AUTO

# def reset_factory(entity, default, call=None, params={}, delay=0):
#   entity_name = entity.split(".")[1]
#   entity_timer = f"timer.{entity_name}"
#   call = call or MAP_SERVICE_HA_TURNOFF

#   @logged
#   def reset():
#     return service.call(call.split(".")[0], call.split(".")[1], entity_id=entity, **params)

#   if delay > 0:
#     @state_trigger(expr(entity, default, '!='), state_check_now=True, state_hold=1)
#     @debugged
#     def timer_start(duration=delay):
#       timer.start(entity_id=entity_timer, duration=delay)
#       return resulted(RESULT_STATUS.STARTED, entity=entity_timer, duration=delay)

#     @event_trigger("timer.finished", f"entity_id == '{entity_timer}'")
#     @state_active(expr(entity_timer, MAP_STATE_HA_TIMER_ACTIVE))
#     @debugged
#     def timer_stop(**kwargs):
#       return resulted(RESULT_STATUS.STOPPED, entity=entity_timer, details=reset())

#     @state_trigger(expr(entity, default), state_check_now=False, state_hold_false=0, state_hold=1)
#     @state_active(expr(entity_timer, MAP_STATE_HA_TIMER_ACTIVE))
#     @debugged
#     def timer_reset(var_name=None, value=None, old_value=None):
#       timer.cancel(entity_id=entity_timer)
#       return resulted(RESULT_STATUS.CANCELED, entity=entity_timer, state=value)

#     trigger.extend([timer_start, timer_stop, timer_reset])
#   else:
#     @state_trigger(expr(entity, default, '!='), state_check_now=True, state_hold=1)
#     def default_reset():
#       reset()
  
# for entity, details in entities.items():
#   reset_factory(entity, details["default"],
#     **{k: v for k, v in details.items() if k in {"call", "params", "delay"}} )

# import regex as re

# from constants.entities import ENTITIES_AUTO
# from constants.mappings import MAP_EVENT_SYSTEM_STARTED, MAP_PERSISTENCE_PREFIX_TIMER, MAP_STATE_HA_TIMER_IDLE, MAP_SERVICE_HA_TURNOFF, MAP_STATE_HA_UNDEFINED
# from constants.settings import SET_ENTITIES_GLOBAL_VOLUME_MAX

# from generic import RESULT_STATUS
# from utils import *

# trigger = []

# entities = ENTITIES_AUTO

# def default_factory(entity, default, call, params):

#   @state_trigger(f"{entity} {'!=' if isinstance(default, str) else 'not in'} {repr(default)} and {entity} != None")
#   def default():
#     service.call(call_service[0],  call.split(".")[1], **{k: v for k, v in params.items()})

# def timeout_factory(entity, default, delay=0):

#   entity_name = entity.split(".")[1]
#   entity_timer = f"timer.{entity_name}"

#   @state_trigger(expr(entity, default, '!='), state_check_now=True, state_hold=1)
#   @debugged
#   def timer_start(duration=delay):
#     timer.start(entity_id=entity_timer, duration=delay)
#     return resulted(RESULT_STATUS.STARTED, entity=entity_timer, duration=delay)

#   @event_trigger("timer.finished", f"entity_id == '{entity_timer}'")
#   @debugged
#   def timer_stop(**kwargs):
#     service.call("homeassistant", f"turn_{default[0] if isinstance(default, list) else default}", entity_id=entity)
#     return resulted(RESULT_STATUS.STOPPED, entity=entity_timer, details=kwargs)

#   @state_trigger(expr(entity, default), state_check_now=False, state_hold_false=0, state_hold=1)
#   @state_active(f"{entity}.old not in {MAP_STATE_HA_UNDEFINED}")
#   @debugged
#   def timer_reset(var_name=None, value=None, old_value=None):
#     timer.cancel(entity_id=entity_timer)
#     return resulted(RESULT_STATUS.CANCELED, entity=entity_timer, state=value)

#   trigger.extend([timer_start, timer_stop, timer_reset])

# for entity, details in entities.items():
#   if "delay" in details:
#     timeout_factory(entity, details["default"], details["delay"])
#   else:
#     details.setdefault("call", MAP_SERVICE_HA_TURNOFF)
#     default_factory(entity, details['default'], details['call'], details['params'])
