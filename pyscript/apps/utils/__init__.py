log_state_trigger = []

def log_state_factory(expr):

  @state_trigger(expr)
  def log_state(trigger_type=None, var_name=None, value=None, old_value=None):  
    log.debug(f"[{var_name}] {trigger_type}: {value} ({old_value})")

  log_state_trigger.append(log_state) 
  
  log.info(f"Logging: {expr}")

@service
def log_state(expr):
  log_state_factory(expr)