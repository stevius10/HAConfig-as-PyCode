from helper import expr
from constants import AUTO_CONFIG_TIMER_DURATION_LUFTREINIGER, AUTO_CONFIG_TIMER_DURATION_SZ_VENTILATOR, AUTO_CONFIG_TIMER_DURATION_SCHLAFZIMMER

timer_trigger = []

entities = {
  "fan.luftreiniger": { "state": "on", "duration": AUTO_CONFIG_TIMER_DURATION_LUFTREINIGER, "timer": "timer.h_timer_luftreiniger" }, 
  "fan.sz_ventilator": { "state": "on", "duration": AUTO_CONFIG_TIMER_DURATION_SZ_VENTILATOR, "timer": "timer.h_timer_sz_ventilator" }, 
  "media_player.schlafzimmer": { "state": "playing", "duration": AUTO_CONFIG_TIMER_DURATION_SCHLAFZIMMER, "timer": "timer.h_timer_schlafzimmer" }, 
}

def timer_factory(entity, entity_state, entity_duration, entity_timer):

  @state_trigger(entity, state_check_now=True)
  def timer_start():
    if state.get(entity) == entity_state:
      timer.cancel(entity_id=entity_timer)
      timer.start(entity_id=entity_timer, duration=entity_duration)
    else:
      timer.cancel(entity_id=entity_timer)
  timer_trigger.append(timer_start)

  @state_trigger(expr(entity_timer, "idle"))
  def timer_stop():
    homeassistant.turn_off(entity_id=entity)
  timer_trigger.append(timer_stop)

for entity in entities:
  timer_factory(entity, entities[entity]["state"], entities[entity]["duration"], entities[entity]["timer"])