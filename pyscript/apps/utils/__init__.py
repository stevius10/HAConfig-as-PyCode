from config import LOG_DEBUG, LOG_DEBUG_DEVICES

log_state_trigger = []

def log_state_factory(entity, expr):

  @state_trigger(f"{entity} {expr}")
  def log_state(trigger_type=None, var_name=None, value=None, old_value=None):  
    log.info(f"[{var_name}] {trigger_type}: {value} ({old_value})")

  if LOG_DEBUG or entity in LOG_DEBUG_DEVICES:
    log_state_trigger.append(log_state) 

  info = f"[automation] {entity}: {expr}"
  try: info += f"({state.get(entity)})" if state.get(entity) is not None else ""
  except: pass 
  log.info(info)
  
@service
def log_state(entity, expr):
  log_state_factory(entity, expr)