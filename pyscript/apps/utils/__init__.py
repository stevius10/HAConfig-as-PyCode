import regex as re

log_state_trigger = []

def log_state_factory(expr):

  @state_trigger(expr)
  def log_state(trigger_type=None, var_name=None, value=None, old_value=None):  
    log.debug(f"[{var_name}] {trigger_type}: {value} ({old_value})")
  
  log.info("+ {}".format(re.sub("and [\w]+\.[\w]+ not in \['.*'\]", "",  expr)))
  log_state_trigger.append(log_state) 

@service
def log_state(expr):
  log_state_factory(expr)