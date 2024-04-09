from config import LOG_DEBUG, LOG_DEBUG_DEVICES, STATES_HA_UNDEFINED

log_state_trigger = []

def log_state_factory(entity, expr):

  @state_trigger(f"{entity} {expr}")
  def log_state(trigger_type=None, var_name=None, value=None, old_value=None):  
    pyscript.log(msg=f"[{var_name}] {trigger_type}: {value} ({old_value})")

  if LOG_DEBUG or entity in LOG_DEBUG_DEVICES:
    log_state_trigger.append(log_state) 
  
  info = f"{entity} {expr}"
  try: info += f" ({state.get(entity)})" if state.get(entity) not in STATES_HA_UNDEFINED else ""
  except: pass
  try: pyscript.log(msg=f"[trigger] {info}")
  except: pass

@service
def log_state(entity, expr):
  log_state_factory(entity, expr)