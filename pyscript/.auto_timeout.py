from constants import AUTO_CONFIG_timeout_SUNSET_DIFF, AUTO_CONFIG_timeout_TIMEOUT, AUTO_CONFIG_timeout_TRANSITION
from helper import expr

entities = { 
  "media_player.schlafzimmer": { "state": "playing", "timeout": 1, "timer": "h_timer_media_sz" }, 
}

timer_trigger = []
timeout_trigger = []

def timer_off_factory(timer, entity):
  @state_trigger(expr(timer, "0"))
  def timer_off(var_name=None):
    homeassistant.turn_off(entity)
    timer_trigger.append()
  timeout_trigger.append(timer_timeout)

def timer_timeout_factory(entity):
  @state_trigger(expr(entity, entity['state']), state_hold=entity['timer'], state_check_now=True)
  def timer_timeout(var_name=None):
    timer.cancel(entity_id=entity['timer'])
    timer.start(entity_id=entity['timer'], duration=entity['timeout'])
    timer_off_factory(entity['timer'], entity)

  timeout_trigger.append(off_timeout)

for entity in entities:
  timer_timeout_factory(entity)