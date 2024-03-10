from constants import LOG_DEBUG_DEVICES

import regex as re

log_state_trigger = []

def log_state_factory(entity, expr):

  @state_trigger(f"{entity} {expr}")
  def log_state(trigger_type=None, var_name=None, value=None, old_value=None):  
    log.info(f"[{var_name}] {trigger_type}: {value} ({old_value})")

  if entity in LOG_DEBUG_DEVICES:
    log_state_trigger.append(log_state) 

  info = f"[+] {entity}: {expr}"
  try: info += f"({state.get(entity)})" if state.get(entity) is not None else ""
  except: pass 
  log.info(info)
  
@service
def log_state(entity, expr):
  log_state_factory(entity, expr)

  # try: 
  #   entity = re.search("^[\w]+\.[\w]\S+", expr).group()
  #   trigger = re.sub("{}".format("and {entity} not in \[\'.*\'\]), "", expr)
  # except Exception as e:
  #   if not entity:
  #     entity = e
  #   if not trigger:
  #     trigger = e
  #   if not entity_state:
  #     entity_state = e
  # finally: 
  #   log.info(" ".join(f"[{entity}]", trigger, state.get(entity)))