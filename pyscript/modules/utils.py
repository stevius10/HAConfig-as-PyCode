from constants.config import LOG_LOGGER_SYS, LOG_LOGGING_LEVEL
from constants.mappings import STATES_UNDEFINED

# Expressions

def expr(entity, expression="", comparator="==", defined=True): 
  
  if isinstance(entity, list) or isinstance(entity, dict):
    return expressions(entities=entity, expression=expression, defined=defined, comparator=comparator)

  statement_condition_defined = f"and {entity} not in {STATES_UNDEFINED}" if defined else ""

  if expression is not None:
    if any([isinstance(expression, (int, float)), '>' in comparator, '<' in comparator]):
      entity = "int({})".format(entity) if entity.isalnum() else 0 # TODO: hardly debuggable
    elif expression in [True, False]: expression = str(expression)
    elif isinstance(expression, str): expression = f"'{expression}'"
    expression = f"{comparator} {expression}"
  else:
    expression = ""

  return f"{entity} {expression} {statement_condition_defined}"
  
def expressions(entities, expression=None, comparator="==", defined=True, operator='or'):  
  if expression:
    if isinstance(expression, int):
      for i in range(len(entities)):
        entities[i] = f"{entities[i]}"
    result = f" {operator} ".join([expr(entity, expression, defined=defined, comparator=comparator) for entity in entities])
  else: 
    result = f" {operator} ".join([f"({expr(entity, expression=None, defined=defined)})" for entity in entities])
  return result

# System Logging

def log(msg="", title="", logger=LOG_LOGGER_SYS, level=LOG_LOGGING_LEVEL):
  if not isinstance(msg, str):
    ns += "".join(getattr(msg, attr, "") for attr in ("get_name", "func_name"))
  if title: message = f"[{title}] {message}"
  system_log.write(message=msg, logger=logger, level=level)
  
def logged(func):
  def wrapper(*args, **kwargs):
    result = func(*args, **kwargs)
    if "context" in kwargs: del kwargs['context']
    parameter_args = ', '.join([str(arg) for arg in args if arg is not None]) if args else None
    parameter_kwargs = ', '.join([f'{k}={v}' for k, v in kwargs.items() if v is not None]) if kwargs else None
    result = str(result) if result is not None else ''
    log(msg=f"{func.name}{f'({parameter_args})' if parameter_args else ''}{f'({parameter_kwargs})' if parameter_kwargs else ''}{f'({result})' if result else ''}")
    return result
  return wrapper

# Helper

# def ctx_call(func):
#   def decorator(ctx):
#     current_ctx = pyscript.get_global_ctx()
#     pyscript.set_global_ctx(ctx)
#     result = func()
#     pyscript.set_global_ctx(current_ctx)
#     return result
#   return decorator