from constants.config import LOG_LOGGER_SYS, LOG_LOGGING_LEVEL
from constants.mappings import STATES_UNDEFINED

import importlib

# Expressions

def expr(entity, expression="", comparator="==", defined=True): 
  
  if isinstance(entity, list) or isinstance(entity, dict):
    return expressions(entities=entity, expression=expression, defined=defined, comparator=comparator)

  statement_condition_defined = f"and {entity} not in {STATES_UNDEFINED}" if defined else ""

  if expression is not None:
    if any([isinstance(expression, (int, float)), '>' in comparator, '<' in comparator]):
      entity = "int({entity})" if entity.isalnum() else 0 # TODO
    elif expression in [True, False]: expression = str(expression)
    elif isinstance(expression, str): expression = f"'{expression}'"
    expression = f"{comparator} {expression}"
  else:
    expression = ""
    
  return f"{entity} {expression} {statement_condition_defined}"

def expressions(entities, expression=None, comparator="==", defined=True, operator='or'):  
  if expression:
    if isinstance(expression, int):
      return f" {operator} ".join([expr(entity, expression, defined=defined, comparator=comparator) for entity in entities])
  else: 
    return f" {operator} ".join([f"{expr(entity, expression=None, defined=defined)}" for entity in entities])

'''
# Expressions

def expr(entity: Union[str, list, dict], expression: Any = "", comparator: str = "==", defined: bool = True) -> str:
  if isinstance(entity, (list, dict)):
    return expressions(entities=entity, expression=expression, defined=defined, comparator=comparator)
  
  statement_condition_defined = f"and str({entity}) not in {STATES_UNDEFINED}" if defined else ""
  expression = build(str(entity), expression, comparator)
  
  return f"{expression} {statement_condition_defined}"

# Helper

def exprs(entities, expression=None, comparator="==", defined=True, operator='or'):  
  if expression:
    if isinstance(expression, int):
      for i in range(len(entities)):
        entities[i] = f"{entities[i]}"
    result = f" {operator} ".join([expr(entity, expression, defined=defined, comparator=comparator) for entity in entities])
  else: 
    result = f" {operator} ".join([f"({expr(entity, expression=None, defined=defined)})" for entity in entities])
  return result

def convert(entity: Any, expression: Any, comparator: str) -> str:
  if isinstance(expression, (int, float)) or any(comparison in comparator for comparison in ('>', '<')):
    return str(int(entity)) if entity is not None and str(entity).isalnum() else "None"
  elif isinstance(expression, bool): return str(expression).lower()
  elif isinstance(expression, str): return f"'{expression}'"
  else: return str(entity)

def build_expression(entity: str, expression: Any, comparator: str) -> str:
  converted = convert(entity, expression, comparator)
  return f"{converted} {comparator} {expression}" if expression is not None else converted
'''
  
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
    result = func(*args, **kwargs)
    if "context" in kwargs: del kwargs['context']
    parameter_args = ', '.join([str(arg) for arg in args if arg is not None]) if args else None
    parameter_kwargs = ', '.join([f'{k}={v}' for k, v in kwargs.items() if v is not None]) if kwargs else None
    result = str(result) if result else ''
    
    if kwargs.get('trigger_type') != 'state' or (kwargs.get('trigger_type') == 'state' and 
      kwargs.get('value') not in STATES_UNDEFINED and kwargs.get('old_value') not in STATES_UNDEFINED):
      log(msg=f"{func.name}{f'({parameter_args})' if parameter_args else ''}{f'({parameter_kwargs})' if parameter_kwargs else ''}{f'({result})' if result else ''}")
    return result
  return wrapper

def debugged(func):
  def wrapper(*args, **kwargs):
    result = func(*args, **kwargs)
    if "context" in kwargs: del kwargs['context']
    parameter_args = ', '.join([str(arg) for arg in args if arg is not None]) if args else None
    parameter_kwargs = ', '.join([f'{k}={v}' for k, v in kwargs.items() if v is not None]) if kwargs else None
    result = str(result) if result is not None else ''
    debug(msg=f"{func.name}{f'({parameter_args})' if parameter_args else ''}{f'({parameter_kwargs})' if parameter_kwargs else ''}{f'({result})' if result else ''}")
    return result
  return wrapper