from constants.config import LOG_LOGGER_SYS, LOG_LOGGING_LEVEL
from constants.mappings import STATES_UNDEFINED

import importlib
import sys
import traceback

# Logging

def debug(msg="", title=""):
  try:
    logfile = importlib.import_module("logfile")
    if title: msg = f"[{title}] {msg}"
    logfile.Logfile.debug(msg)
  except ModuleNotFoundError:
    pass  # Avoid validation before sys.path appended

def log(msg="", title="", logger=None, level=LOG_LOGGING_LEVEL, **kwargs):
  if msg and isinstance(msg, str):
    if title: msg = f"[{title}] {msg}"
    if msg: 
      logger = f"{LOG_LOGGER_SYS}.{logger}" if logger else LOG_LOGGER_SYS
      system_log.write(message=msg, logger=LOG_LOGGER_SYS, level=level)

def _monitored(func, log_func):
  def wrapper(*args, **kwargs):
    if kwargs.get('context'): del kwargs['context']
    title = f"{func.global_ctx_name}:{func.name}"
    debug(f"{log_func_format(func, args, kwargs)}", title=title) # debug
    try:
      result = func(*args, **kwargs)
    except Exception as e:
      result = f"{type(e)}: {str(e)}"
    finally:
      if log_func == "log":
        log(log_func_format(func, args, kwargs, result), logger=title)
      debug(log_func_format(func, args, kwargs, result), title=title)
    return result or ""
  return wrapper

def debugged(func):
  return _monitored(func, "debug")

def logged(func):
  return _monitored(func, "log")

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
    if isinstance(expression, list):
      if comparator is None or comparator == "==":
        conditions.append(f"{entity} in {expression}")
      else:
        conditions.append(f"{entity} not in {expression}")
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

def log_func_format(func, args, kwargs, result=None):
  log_func_format_args = ", ".join([str(arg) if arg else "" for arg in args]) if args else None
  log_func_format_kwargs = ", ".join([f"{k}={v}" for k, v in kwargs.items() if k is not "context"]) if kwargs else None
  log_func_format_arg = ", ".join([str(arg) if arg is not None else "" for arg in [log_func_format_args, log_func_format_kwargs] if arg])
  return f"{func.name}" + f"({log_func_format_arg})" + (f": \n-> {result}" if result else "")