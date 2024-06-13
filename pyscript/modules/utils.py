from constants.config import LOG_LOGGER_SYS, LOG_LOGGING_LEVEL
from constants.mappings import STATES_UNDEFINED

import importlib

# Expressions

def expr(entity, expression="", comparator="==", defined=True): 
  
  if isinstance(entity, list) or isinstance(entity, dict):
    return exprs(entities=entity, expression=expression, defined=defined, comparator=comparator)

  statement_condition_defined = f"and {entity} not in {STATES_UNDEFINED}" if defined else ""

  if expression is not None:
    if isinstance(expression, (int, float)) or comparator in ['<', '>']:
      entity = "int({})".format(entity)
    if expression in [True, False]: expression = str(expression)
    elif isinstance(expression, str): expression = f"'{expression}'"
    expression = f"{comparator} {expression}"
  else:
    expression = ""
    
  return f"{entity} {expression} {statement_condition_defined}"

def exprs(entities, expression=None, comparator="==", defined=True, operator='or'):  
  if expression:
    if isinstance(expression, int):
      expressions = f" {operator} ".join([f"({expr(entity, expression, defined=defined, comparator=comparator)})" for entity in entities])
    else: 
      expressions = f" {operator} ".join([f"({expr(entity, expression=expression, defined=defined)})" for entity in entities])
  return expressions

# Logging

def log(msg="", title="", logger=LOG_LOGGER_SYS, level=LOG_LOGGING_LEVEL):
  if not isinstance(msg, str):
    logger += "".join([getattr(msg, attr, "") for attr in ("get_name", "func_name")])
  if title: message = f"[{title}] {message}"
  system_log.write(message=msg, logger=logger, level=level)

def debug(msg=""):
    logfile = importlib.import_module("logfile") # except: pass # on purpose: avoid validate before sys.path appended
    logfile.Logfile.debug(msg)

def logged(func):
  def wrapper(*args, **kwargs):
    logged = func(*args, **kwargs)
    if "context" in kwargs: del kwargs['context']
    parameter_args = ', '.join([str(arg) for arg in args if arg is not None]) if args else None
    parameter_kwargs = ', '.join([f'{k}={v}' for k, v in kwargs.items() if v is not None]) if kwargs else None
    logged = str(logged) if logged else ''
    
    if kwargs.get('trigger_type') != 'state' or (kwargs.get('trigger_type') == 'state' and 
      kwargs.get('value') not in STATES_UNDEFINED and kwargs.get('old_value') not in STATES_UNDEFINED):
      log(msg=f"{func.name}{f'({parameter_args})' if parameter_args else ''}{f'({parameter_kwargs})' if parameter_kwargs else ''}{f': {logged}' if logged else ''}")
    return logged
  return wrapper

def debugged(func):
  def wrapper(*args, **kwargs):
    debugged = func(*args, **kwargs)
    if "context" in kwargs: del kwargs['context']
    parameter_args = ', '.join([str(arg) for arg in args if arg is not None]) if args else None
    parameter_kwargs = ', '.join([f'{k}={v}' for k, v in kwargs.items() if v is not None]) if kwargs else None
    result = str(debugged) if debugged is not None else ''
    debug(msg=f"{func.name}{f'({parameter_args})' if parameter_args else ''}{f'({parameter_kwargs})' if parameter_kwargs else ''}{f': {debugged})' if debugged else ''}")
    return debugged
  return wrapper