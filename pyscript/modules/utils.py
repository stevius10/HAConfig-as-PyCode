from constants.config import LOG_LOGGER_SYS, LOG_LOGGING_LEVEL
from constants.mappings import STATES_UNDEFINED

import importlib
  
# Logging

def debug(msg=""):
    try: 
      logfile = importlib.import_module("logfile") 
      logfile.Logfile.debug(msg)
    except ModuleNotFoundError: 
      pass # on purpose: avoid validation before sys.path appended

def log(msg="", title="", logger=LOG_LOGGER_SYS, level=LOG_LOGGING_LEVEL):
  if not isinstance(msg, str):
    logger += "".join([getattr(msg, attr, "") for attr in ("get_name", "func_name")])
  if title: message = f"[{title}] {message}"
  system_log.write(message=msg, logger=logger, level=level)
  debug(msg)

def debugged(func):
  def wrapper(*args, **kwargs):
    if "context" in kwargs: del kwargs["context"]
    debugged_result = func(*args, **kwargs)
    
    parameter_args = ", ".join([str(arg) for arg in args if arg is not None]) if args else None
    parameter_kwargs = ", ".join([f"{k}={v}" for k, v in kwargs.items() if v is not None]) if kwargs else None
    debug(msg=f"{func.name}{f'({parameter_args})' if parameter_args else ''}{f'({parameter_kwargs})' if parameter_kwargs else ''}{f': {debugged_result}' if debugged_result else ''}")
    return debugged_result
  return wrapper

def logged(func):
  def wrapper(*args, **kwargs):
    if "context" in kwargs: del kwargs["context"]
    logged_result = func(*args, **kwargs)

    parameter_args = ", ".join([str(arg) for arg in args if arg is not None]) if args else None
    parameter_kwargs = ", ".join([f"{k}={v}" for k, v in kwargs.items() if v is not None]) if kwargs else None
    if kwargs.get("trigger_type") != "state" or ( kwargs.get("trigger_type") == "state" and 
      kwargs.get("value") not in STATES_UNDEFINED and kwargs.get("old_value") not in STATES_UNDEFINED):
      log(msg=f"{func.name}{f"({parameter_args})" if parameter_args else ""}{f"({parameter_kwargs})" if parameter_kwargs else ""}{f": {logged_result}" if logged_result else ''}", logger=f"{LOG_LOGGER_SYS}.{func.name}")
    return logged_result
  return wrapper

# Expressions

@debugged
def expr(entity, expression="", comparator="==", defined=True, operator='or'):
  if isinstance(entity, (list, dict)):
    items = [f"({expr(item, expression, comparator, defined)})" for item in entity]
    return f" {operator} ".join(items)

  conditions = []
  
  if defined:
    conditions.append(f"{entity} is not None")
    states_undefined_str = ", ".join([f'\"{state}\"' for state in STATES_UNDEFINED])
    conditions.append(f"{entity} not in [{states_undefined_str}]")
      
  if expression:
    if isinstance(expression, (int, float)) or comparator in ['<', '>']:
      conditions.append(f"int({entity}) {comparator} {expression}")
    elif isinstance(expression, str):
      conditions.append(f"{entity} {comparator} \'{expression}\'")
    else:
      conditions.append(f"{entity} {comparator} {expression}")
  else:
    conditions.append(f"{entity}")

  return " and ".join(conditions)

# Utility

def logs(obj):
  if isinstance(obj, str):
    return obj
  elif isinstance(obj, dict):
    items = []
    for k in obj.keys():
      items.append(f"{k}={logs(obj.get(k, ''))}")
    return ", ".join(items)
  elif isinstance(obj, (list, tuple)):
    items = [logs(item) for item in obj]
    return f"[{', '.join(items)}]"
  else:
    try:
      attributes = vars(obj)
      attrs = []
      for key in attributes.keys():
        attrs.append(f"{key}={logs(attributes.get(key, ''))}")
      return f"{type(obj).__name__}({', '.join(attrs)})"
    except TypeError:
      return str(obj)