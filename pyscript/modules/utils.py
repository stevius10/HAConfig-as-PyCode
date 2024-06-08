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
    log(result)
  return result

# System Logging

def log(msg="", ns=None, ctx=None, title="", level=LOG_LOGGING_LEVEL):
  if not isinstance(msg, str) and hasattr(msg, "get_name"): ns += msg.get_name()
  if not isinstance(msg, str) and hasattr(msg, "func_name"): ns += msg.get("func_name")
  if ns is None: ns = LOG_LOGGER_SYS
  # if ctx is None: ctx=pyscript.get_global_ctx()
  @ctx_call
  def ctx_debug(ctx=ctx):
    def debug(ctx): 
      return f"{globals()['__name__']} ({ctx.replace('.', '/')}.py)" 
    return debug(ctx)
  if not isinstance(msg, str) and hasattr(msg, "get_name"): 
    ns += msg.get_name()
  if not isinstance(msg, str) and hasattr(msg, "func_name"): 
    ns += msg.get("func_name")
  message = ": ".join([f"{ctx.replace('.', '/')}.py", msg]) if ctx else msg
  if title: message = f"[{title}] {message}"
  system_log.write(message=msg, logger=ns, level=level)

def call_func(func, **kwargs):
  if service.has_service(func.split(".")[0], func.split(".")[1]):
    service.call(func.split(".")[0], func.split(".")[1], **kwargs)

def ctx_call(func):
  def decorator(ctx):
    current = pyscript.get_global_ctx()
    pyscript.set_global_ctx(ctx)
    result = func()
    pyscript.set_global_ctx(current)

    return result
  return decorator

def log_context(func):
  def wrapper(*args, **kwargs):
    return func(*args, **kwargs, ns=func.name)
  return wrapper

def set_log_context(ctx=pyscript.get_global_ctx()):
  global logs
  logs = lambda msg="", level=LOG_LOGGING_LEVEL, logger=LOG_LOGGER_SYS, ctx=ctx: log(msg, level, logger, ctx)