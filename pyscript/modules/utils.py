import importlib
import sys 

from constants.config import CFG_LOG_LOGGER, CFG_LOG_LEVEL, CFG_LOGFILE_DEBUG_FUNCTION_STARTED, CFG_LOGFILE_IMPORT_RETRIES, CFG_LOGFILE_IMPORT_TIMEOUT, CFG_PATH_DIR_PY_NATIVE
from constants.mappings import MAP_STATE_HA_UNDEFINED, MAP_EVENT_SYSTEM_STARTED

from generic import ForwardException

# Logging

def debug(msg="", title=""):
  if msg := f"[{title}] {msg}" if title else msg:
    try:
      get_logfile().debug(msg)
    except: pass # avoid startup validation

def log(msg="", title="", logger=CFG_LOG_LOGGER, level=CFG_LOG_LEVEL, **kwargs):
  if msg := f"[{title}] {msg}" if title else msg:
    system_log.write(message=str(msg), logger=logger, level=level)

# Monitoring 

def _observed(func, log_func, debug_function_started=CFG_LOGFILE_DEBUG_FUNCTION_STARTED):
  def wrapper(*args, **kwargs):
    log_title = func.global_ctx_name if hasattr(func, 'global_ctx_name') and hasattr(func, 'name') else ""
    kwargs.pop('context', None)
    debug_function_started and debug(format_observed(func, args, kwargs), title=log_title)
    try:
      result = func(*args, **kwargs)
      log_func == "log" and result and log(format_observed(func, args, kwargs, result), title=log_title)
      debug(format_observed(func, args, kwargs, result), title=log_title)
      return result
    except Exception as e:
      raise ForwardException(e, func.global_ctx_name)

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

def expr(entity, expression="", comparator="==", defined=True, previous=False, operator='or'):
  if entity and not isinstance(entity, str):
    if isinstance(entity, list):
      items = [f"({expr(item, expression, comparator, defined, previous)})" for item in entity]
    if isinstance(entity, dict):
      items = [f"({expr(key, value, expression, comparator, defined, previous)})" for key, value in entity.items()]
    return f" {operator} ".join(items) if items else None

  conditions = []
  
  states_undefined_str = ", ".join([f' \"{state}\" ' for state in MAP_STATE_HA_UNDEFINED])
  if defined:
    conditions.append(f'{entity} is not None and {entity} not in [{states_undefined_str}]')

  if previous:
    if isinstance(previous, bool):
      conditions.append(f'{entity}.old is not None and {entity}.old not in [{states_undefined_str}]')
    else:
      if isinstance(entity, dict):
        items = [f"({expr(f'{key}.old', value, comparator=comparator, defined=defined)})" for key, value in entity.items()]
        conditions.append(f" {operator} ".join(items))
      elif isinstance(entity, list):
        items = [f"({expr(f'{item}.old', previous, comparator=comparator, defined=defined)})" for item in entity]
        conditions.append(f" {operator} ".join(items))
      else:
        conditions.append(f"{entity}.old {comparator} '{previous}'")


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
    state.set(entity, value[:255], kwargs if kwargs else {})
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
  return f"{func.name if hasattr(func, 'name') else ''}({", ".join(filter(None, [str_args, str_kwargs]))})" + (f": -> {result}" if result else "")
