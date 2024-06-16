from constants.config import LOG_LOGGER_SYS, LOG_LOGGING_LEVEL
from constants.mappings import STATES_UNDEFINED

import importlib


  
# Logging

def debug(msg=""):
    logfile = importlib.import_module("logfile") # except: pass # on purpose: avoid validate before sys.path appended
    logfile.Logfile.debug(msg)

def log(msg="", title="", logger=LOG_LOGGER_SYS, level=LOG_LOGGING_LEVEL):
  if not isinstance(msg, str):
    logger += "".join([getattr(msg, attr, "") for attr in ("get_name", "func_name")])
  if title: message = f"[{title}] {message}"
  system_log.write(message=msg, logger=logger, level=level)
  debug(msg)

def debugged(func):
  def wrapper(*args, **kwargs):
    #if "context" in kwargs:
      #kwargs["context"] = func.name
    debugged_result = func(*args, **kwargs)
    
    parameter_args = ", ".join([str(arg) for arg in args if arg is not None]) if args else None
    parameter_kwargs = ", ".join([f"{k}={v}" for k, v in kwargs.items() if v is not None]) if kwargs else None
    debug(msg=f"{func.name}{f'({parameter_args})' if parameter_args else ''}{f'({parameter_kwargs})' if parameter_kwargs else ''}{f': {debugged_result}' if debugged_result else ''}")
    return debugged_result
  return wrapper

def logged(func):
  def wrapper(*args, **kwargs):
    if "context" in kwargs: kwargs["context"] = func.name
    logged_result = func(*args, **kwargs)

    parameter_args = ", ".join([str(arg) for arg in args if arg is not None]) if args else None
    parameter_kwargs = ", ".join([f"{k}={v}" for k, v in kwargs.items() if v is not None]) if kwargs else None
    if kwargs.get("trigger_type") != "state" or ( kwargs.get("trigger_type") == "state" and 
      kwargs.get("value") not in STATES_UNDEFINED and kwargs.get("old_value") not in STATES_UNDEFINED):
      log(msg=f"{func.name}{f"({parameter_args})" if parameter_args else ""}{f"({parameter_kwargs})" if parameter_kwargs else ""}{f": {logged_result}" if logged_result else ''}")
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

    return " and ".join(conditions)

# Utility

def log_data(*args, **kwargs):
  data = {}
  for arg in args:
    data[f'var_{len(data)}'] = arg
  for key, value in kwargs.items():
    if isinstance(value, object):
      try: data[key] = vars(value)
      except TypeError: data[key] = str(value)
    else: data[key] = value
  log(msg=data, title=kwargs.pop('', log_data.context))