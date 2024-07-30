import importlib
import sys 

from constants.config import CFG_LOG_LOGGER, CFG_LOG_LEVEL, CFG_LOGFILE_DEBUG_FUNCTION_STARTED, CFG_LOGFILE_IMPORT_RETRIES, CFG_LOGFILE_IMPORT_TIMEOUT, CFG_PATH_DIR_PY_NATIVE
from constants.mappings import MAP_STATE_HA_UNDEFINED

from generic import ForwardException

# Logging

def debug(msg="", title=""):
  if title: 
    msg = f"[{title}] {msg}"
  if msg:
    try:
      logfile = get_logfile()
      logfile.debug(msg)
    except: # avoid startup validation
      pass  # handled functional

def log(msg="", title="", logger=CFG_LOG_LOGGER, level=CFG_LOG_LEVEL, **kwargs):
  if title: 
    msg = f"[{title}] {msg}"
  if msg: 
    system_log.write(message=str(msg), logger=logger, level=level)

# Monitoring 

def _observed(func, log_func, debug_function_started=CFG_LOGFILE_DEBUG_FUNCTION_STARTED):
  def wrapper(*args, **kwargs):
    if kwargs.get('context'): del kwargs['context']
    context = ".".join([func.global_ctx_name, func.name]) if hasattr(func, 'global_ctx_name') and hasattr(func, 'name') else ""
    if debug_function_started:
      debug(f"{format_observed(func, args, kwargs)}", title=context)
    try:
      result = func(*args, **kwargs)
    except Exception as e:
      raise ForwardException(e, context)
    finally:
      # if result:
      if log_func == "log":
        log(format_observed(func, args, kwargs, result), title=context)
      debug(format_observed(func, args, kwargs, result), title=context)
    return result
  return wrapper

def debugged(func):
  return _observed(func, "debug")

def logged(func):
  return _observed(func, "log")

def resulted(status, entity=None, message=None, **kwargs):
  return { "status": status.value,
    **({"entity": entity} if entity else {}),
    **({"message": message} if message else {}),
    **({"details": kwargs} if kwargs else {}) }

# Functional 

@debugged
def expr(entity, expression="", comparator="==", defined=True, operator='or'):
  if entity and not isinstance(entity, str):
    if isinstance(entity, list):
      items = [f"({expr(item, expression, comparator, defined)})" for item in entity]
    if isinstance(entity, dict):
      items = [f"({expr(key, value, expression, comparator, defined)})" for key, value in entity.items()]
    return f" {operator} ".join(items) if items else None

  conditions = []
  if defined:
    states_undefined_str = ", ".join([f' \"{state}\" ' for state in MAP_STATE_HA_UNDEFINED])
    conditions.append(f'{entity} is not None and {entity} not in [{states_undefined_str}]')
      
  if expression:
    if isinstance(expression, list):
      if comparator in [None, "==", "in"]:
        conditions.append(f"{entity} in {expression}")
      elif comparator in ["!=", "not"]:
        conditions.append(f"{entity} not in {expression}")
    if isinstance(expression, (int, float)) or comparator in ['<', '>']:
      conditions.append(f"int(float({entity})) {comparator} {expression}")
    elif isinstance(expression, str):
      conditions.append(f"{entity} {comparator} \'{expression}\'")
  else:
    conditions.append(f"{entity}")

  return " and ".join(conditions)

# Persistence

def store(entity, value=None, result=True, **kwargs): 

  if value is not None:
    state.set(entity, value, kwargs if kwargs else {})
    homeassistant.update_entity(entity_id=entity)
    state.persist(entity)
  else: 
    state.persist(entity, default_value="")

  if result:
    homeassistant.update_entity(entity_id=entity)
    entity_state = state.get(entity)
    return entity_state
  
# Utility

def get_logfile(name=None):
  logfile = None
  for attempt in range(CFG_LOGFILE_IMPORT_RETRIES):
    try:
      from logfile import Logfile
      logfile = Logfile(name if name else None)
      return logfile
    except Exception as e:
      if attempt < CFG_LOGFILE_IMPORT_RETRIES - 1: 
        task.wait_until(event_trigger=MAP_EVENT_SYSTEM_STARTED, timeout=CFG_LOGFILE_IMPORT_TIMEOUT)
      else: 
        raise e

def format_observed(func, args, kwargs, result=None):
  str_args = ", ".join([str(arg) if arg is not None else "" for arg in args]) if args else ""
  str_kwargs = ", ".join([f"{k}={v}" for k, v in kwargs.items() if k != "context"]) if kwargs else ""
  return f"{func.name if hasattr(func, 'name') else ''}({", ".join(filter(None, [str_args, str_kwargs]))})" + (f": \n-> {result}" if result else "")
