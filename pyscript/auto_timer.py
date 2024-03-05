from helper import expr

entities = {
  "fan.luftreiniger": { "state": "playing", "timeout": 60, "timer": "timer.h_timer_luftreiniger" }, 
  "fan.sz_ventilator": { "state": "playing", "timeout": 60, "timer": "timer.h_timer_sz_ventilator" }, 
  "media_player.schlafzimmer": { "state": "playing", "timeout": 60, "timer": "h_timer_media_sz" }, 
}

timer_off_trigger = []
timer_timeout_trigger = []

def timer_timeout_factory(entity, entity_state, entity_timeout, entity_timer):
  @state_trigger(expr(entity, entity_state), state_check_now=True)
  def timer_timeout(var_name=None):
    timer.cancel(entity_id=entity_timer)
    timer.start(entity_id=entity_timer, duration=entity_timeout)
    timer_off_factory(entity_timer, entity)
  timer_timeout_trigger.append(timer_timeout)

def timer_off_factory(entity, entity_state, entity_timeout, entity_timer):
  @state_trigger(expr(entity_timer, "0"))
  def timer_off(var_name=None):
    homeassistant.turn_off(entity)
  timer_off_trigger.append(timer_off)
  timer_timeout_factory(entity, entity_state, entity_timeout, entity_timer)

for entity in entities:
  timer_off_factory(entity, entities[entity]["state"], entities[entity]["timeout"], entities[entity]["timer"])