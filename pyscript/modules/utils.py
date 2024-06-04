from config import LOG_ENABLED, LOG_LOGGING_LEVEL, LOG_LOGGER_SYS
from constants import *

import datetime
import logging
import os
import regex as re

def expr(entity, expression="", comparator="==", defined=True, logs=LOG_ENABLED): 
  
  if isinstance(entity, list) or isinstance(entity, dict):
    return expressions(entities=entity, expression=expression, defined=defined, logs=logs, comparator=comparator)

  statement_condition_defined = f"and {entity} not in {STATES_HA_UNDEFINED}" if defined else ""

  if expression is not None:
    if any([isinstance(expression, (int, float)), '>' in comparator, '<' in comparator]):
      entity = "int({})".format(entity) if entity.isalnum() else 0
    elif expression in [True, False]: expression = str(expression)
    elif isinstance(expression, str): expression = f"'{expression}'"
    expression = f"{comparator} {expression}"
  else:
    expression = ""
  
  if logs: 
    try: pyscript.log_state(expression=f"{entity} {expression}")
    except: pass
  
  return f"{entity} {expression} {statement_condition_defined}"
  
def expressions(entities, expression=None, comparator="==", defined=True, operator='or', logs=LOG_ENABLED):  
  if expression:
    if isinstance(expression, int):
      for i in range(len(entities)):
        entities[i] = f"{entities[i]}"

    result = f" {operator} ".join([expr(entity, expression, defined=defined, logs=False, comparator=comparator) for entity in entities])
  else: 
    result = f" {operator} ".join([expr(entity, expression=None, defined=defined, logs=False) for entity in entities])
    
  if logs: 
    try: pyscript.log_state(expression=result)
    except: pass

  return result

# Function

def log(msg="", ns=None, ctx=None, title="", level=LOG_LOGGING_LEVEL):
  if not isinstance(msg, str) and hasattr(msg, "get_name"): ns += msg.get_name()
  if not isinstance(msg, str) and hasattr(msg, "func_name"): ns += msg.get("func_name")
  #if ns is None: ns = LOG_LOGGER_SYS
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
  # @ctx_call
  # def ctx_debug(ctx=ctx):
  #   def debug(ctx): 
  #     return f"{globals()['__name__']} ({ctx.replace('.', '/')}.py)" 
  #   return debug(ctx)
  message = ": ".join([f"{ctx.replace('.', '/')}.py", msg]) if ctx else msg
  if title: message = f"[{title}] {message}"
  log_internal(msg=message, logger=get_logger(ns))

# Class

class Logfile:
  def __init__(self, ctx):
    self.ctx = ctx
    self.name = ctx.split(".")[1]
    self.logger = logging.getLogger(self.name)
    self.logs = []
    self.logfile = os.path.join(PATH_DIR_PY_LOG, self.name) + ".log"
    handler = logging.FileHandler(self.logfile, mode='w+')
    handler.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))
    self.logger.addHandler(handler)
    self.logger.setLevel(logging.DEBUG)
    self.logger.propagate = False
    await self.truncate()
    self.log("# {}".format(datetime.datetime.now()))
    
  def log(self, message=None):
    if isinstance(message, str):
      if message is not None: # re.search('[a-zA-Z]', message): 
        self.logger.info(message)
        self.logs.append(message)
    elif isinstance(message, list): 
      for msg in message:
        self.log(msg.replace("\n", ""))
      self.log(" ")
    elif message == " ":
        self.logger.info('\n')
        
  def truncate(self):
    call_func("pyscript.log_truncate", logfile=self.logfile, blocking=True)
  
  def finished(self):
    logs = "\n".join(self.logs)
    log(f"{logs.replace("\n", " ")}", ctx=self.ctx, ns=self.name)
    self.log(message=logs)
    return { "service": {self.name}, "logs": logs }

# Helper

def call_func(func, **kwargs):
  if service.has_service(func.split(".")[0], func.split(".")[1]):
    service.call(func.split(".")[0], func.split(".")[1], **kwargs)

def ctx_call(func):
  def decorator(ctx):
    current = pyscript.get_global_ctx()
    pyscript.set_global_ctx(ctx)
    result = func()
    log_internal(msg=f"{func} returned {result} in {ctx} from {current}", logger=get_logger())
    pyscript.set_global_ctx(current)

    return result
  return decorator
  
def get_logger(logger=None):
  return ".".join(filter(None, [LOG_LOGGER_SYS, logger]))
  
def get_trigger_expression(expression):
  pattern = r"and .*? not in \[{}\]".format(", ".join(["'{}'".format(state) for state in STATES_HA_UNDEFINED]))
  return re.sub(pattern, "", expression)#.replace(" ", "")

def log_context(func):
  def wrapper(*args, **kwargs):
    return func(*args, **kwargs, ns=func.name)
  return wrapper
  
def log_internal(msg="", logger=LOG_LOGGER_SYS, level=LOG_LOGGING_LEVEL):
  call_func(SERVICE_HA_SYSLOG_WRITE, message=msg, logger=logger, level=level)

def set_log_context(ctx=pyscript.get_global_ctx()):
  global logs
  logs = lambda msg="", level=LOG_LOGGING_LEVEL, logger=LOG_LOGGER_SYS, ctx=ctx: log(msg, level, logger, ctx)