from helper import expr
from configuration import AUTO_DEFAULT_ENTITIES

from homeassistant.const import EVENT_HOMEASSISTANT_STARTED

reset_trigger = []

entities = AUTO_DEFAULT_ENTITIES

# Defaults

def reset_factory(entity, default, delay=None):

  @event_trigger(EVENT_HOMEASSISTANT_STARTED) # @time_trigger('startup')
  @state_trigger(expr(entity, f"!= '{entities.get(entity)['default']}'"))
  def reset_default(trigger_type=None, var_name=None):
    if state.get(entity) != default:
      if trigger_type == "time" or delay == None: 
        log.info("Default")
        reset(entity, default)
        
      if delay in entities.get(entity): 
        log.info("Add timer" + entity)
        entity_timer = get_timer(entity, delay)
        timer.cancel(entity_id=entity_timer)
        timer.start(entity_id=entity_timer, duration=delay)

  reset_trigger.append(reset_default)

  @event_trigger("timer.finished")
  def timer_stop(**kwargs):
    log.info(f"kwargs: {kwargs}")
    # reset(entity_id=entity)
    
  reset_trigger.append(timer_stop)
  
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
  reset_factory(entity, entities[entity]["default"], entities[entity]["delay"])