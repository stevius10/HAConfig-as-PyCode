from helper import expr
from timeout import AUTO_TIMEOUT_ENTITIES

from homeassistant.const import EVENT_HOMEASSISTANT_STARTED

timeout_trigger = []

entities = AUTO_TIMEOUT_ENTITIES

def timeout_factory(entity, default, delay=None):

  @event_trigger(EVENT_HOMEASSISTANT_STARTED) 
  @state_trigger(expr(entity, expression=entities.get(entity)['default'], comparator="!="))
  def timeout_default(trigger_type=None, var_name=None):
    if state.get(entity) != default:
      if trigger_type == "time" or delay == None: 
        reset(entity, default)
        
      if delay in entities.get(entity): 
        entity_timer = get_timer(entity, delay)
        timer.cancel(entity_id=entity_timer)
        timer.start(entity_id=entity_timer, duration=delay)

  timeout_trigger.append(timeout_default)

  @event_trigger("timer.finished")
  def timer_stop(**kwargs):
    log.info(f"kwargs: {kwargs}")
    # reset(entity_id=entity)
    
  timeout_trigger.append(timer_stop)
  
# Helper

def reset(entity, default):
  if default in ["off"]:
    homeassistant.turn_off(entity_id=entity)
  elif default == "on":
    homeassistant.turn_on(entity_id=entity)
  state.set(entity, default)

def get_timer(entity, delay):
  name = f"pyscript.timer_reset"
  state.set(name, str(delay), device_class='duration', state_class='measurement', unit_of_measurement='m')
  return name

# Initialization
for entity in entities:
  timeout_factory(entity, entities[entity]["default"], entities[entity]["delay"])