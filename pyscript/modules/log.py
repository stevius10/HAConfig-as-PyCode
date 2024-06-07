from constants import *
import logging
import os
from pathlib import Path
import datetime

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
    #await self.truncate()
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
  
  def finished(self):
    logs = "\n".join(self.logs)
    log(f"{logs.replace("\n", " ")}", ctx=self.ctx, ns=self.name)
    self.log(message=logs)
    return { "service": {self.name}, "logs": logs }


# System Log 

def log(msg="", ns=None, ctx=None, title="", level=LOG_LOGGING_LEVEL):
  if not isinstance(msg, str) and hasattr(msg, "get_name"): ns += msg.get_name()
  if not isinstance(msg, str) and hasattr(msg, "func_name"): ns += msg.get("func_name")
  if ns is None: ns = LOG_LOGGER_SYS
  if ctx is None: ctx=pyscript.get_global_ctx()
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