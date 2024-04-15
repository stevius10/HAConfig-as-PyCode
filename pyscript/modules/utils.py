from config import LOG_LOGGING_LEVEL, LOG_SYS_LOGGER, PATH_LOGS, LOG_DEBUG, LOG_DEBUG_DEVICES, STATES_HA_UNDEFINED
from mapping import FUNC_SYSLOG
from helper import expr

import datetime
import functools
import inspect
import logging
import os
import regex as re
import sys

log_state_trigger = []

# Function

def call(func, **kwargs):
  if service.has_service(func.split(".")[0], func.split(".")[1]):
    service.call(func.split(".")[0], func.split(".")[1], **kwargs)

def log(msg, level=LOG_LOGGING_LEVEL, logger=LOG_SYS_LOGGER, ctx=pyscript.get_global_ctx()):
  # debug information
  for finfo in reversed(inspect.stack()[1:]):
    frame = finfo.frame
    filename = frame.f_code.co_filename.split("/")[-1]
    function_name = frame.f_code.co_name
    line_number = frame.f_lineno
    debug_var = frame.f_locals
  debug = f" | {function_name} ({filename}:{line_number})" if function_name != "ast_call" else ""
  
  if not isinstance(msg, str): 
    try: msg += msg.get_name(); msg += msg.get("func_name");
    except: msg += msg.get("func_name");
  
  call(FUNC_SYSLOG, message=f"{msg} {debug}", logger=logger, level=level)
  # call(FUNC_SYSLOG, message=f"{function_name}: {debug_var}", logger=logger, level="debug")

def log_func(func):
  def wrapper(*args, **kwargs):
    func_name = func if isinstance(func, str) else func.get_name()
    if "context" in kwargs:
      del kwargs["context"]
    try:
      ctx = pyscript.get_global_ctx()
      result = func(*args, **kwargs)
    except Exception as e:
      result = f"Error: {e}"
    finally:
      log_module("[{}{}] {} ({}, {}])".format(f"{func_name}", f":({ctx})", f"{result}", f"{args}", f", [{kwargs}]"))
      return result
  return wrapper
  
# Factory

def log_state_factory(entity, expression):
  @state_trigger(expr(entity, expression, defined=True))
  def log_state(trigger_type=None, var_name=None, value=None, old_value=None):  
    if old_value not in STATES_HA_UNDEFINED:
      log(f"[{var_name}] {trigger_type}: {value} ({old_value})")

  if LOG_DEBUG or entity in LOG_DEBUG_DEVICES:
    log_state_trigger.append(log_state) 
  info = expr(entity, expression)
  info = " and ".join(info.split(" and ")[:-1]) if (" not in ") in info.split(" and ")[-1] else info
  try: info += f" ({state.get(entity)})" if state.get(entity) not in STATES_HA_UNDEFINED else ""
  except: pass
  log(f"[trigger] {info}")
@service
def log_state(entity, expr):
  log_state_factory(entity, expression=expr)

# Class

class Logfile:
  def __init__(self, name):
    self.name = name.split(".")[1]
    self.logger = logging.getLogger(self.name)
    self.logs = []
    self.logfile = os.path.join(PATH_LOGS, self.name) + ".log"
    handler = logging.FileHandler(self.logfile, mode='w+')
    handler.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))
    self.logger.addHandler(handler)
    self.logger.setLevel(logging.DEBUG)
    self.logger.propagate = False
    await self.truncate()
    self.log("# {}".format(datetime.datetime.now()))
    
  def log(self, message=None):
    if isinstance(message, str):
      if re.search('[a-zA-Z]', message): 
        self.logger.info(message)
        self.logs.append(message)
    elif isinstance(message, list): 
      for msg in message:
        self.log(msg.replace("\n", ""))
      self.log(" ")
    elif message == " ":
        self.logger.info('\n')
        
  def truncate(self):
    call("pyscript.log_truncate", logfile=self.logfile, blocking=True, logger=self.logger)
  
  def finished(self):
    logs = "\n".join(self.logs)
    log(f"[executed] {self.name}: {logs}")
    self.log(message=logs)
    return { "service": {self.name}, "logs": logs }