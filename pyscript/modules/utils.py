from config import LOG_SYS_LOGGER, PATH_LOGS, LOG_DEBUG, LOG_DEBUG_DEVICES, STATES_HA_UNDEFINED
from helper import expr

import datetime
import functools
import logging
import os
import regex as re
import sys

log_state_trigger = []

def log(msg, level="info", logger=LOG_SYS_LOGGER, ctx=pyscript.get_global_ctx()):
  if msg is None:
    msg = sys._getframe(1).f_code.co_name
  if msg is not None and not isinstance(msg, str): 
    msg = msg.get_name()
  try: pyscript.log(msg=f"{ctx}: {msg}", logger=logger, level=level)
  except: pass

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
      log("{} ({}) {} {}[{}])".format(ctx, func_name, result, args, kwargs))
      return result
  return wrapper

def log_state_factory(entity, expression):
  @state_trigger(expr(entity, expression, defined=True))
  def log_state(trigger_type=None, var_name=None, value=None, old_value=None):  
    if old_value not in STATES_HA_UNDEFINED:
      log(f"[{var_name}] {trigger_type}: {value} ({old_value})")

  if LOG_DEBUG or entity in LOG_DEBUG_DEVICES:
    log_state_trigger.append(log_state) 
  info = expr(entity, expression)
  try: info += f" ({state.get(entity)})" if state.get(entity) not in STATES_HA_UNDEFINED else ""
  except: pass
  try: log(f"[trigger] {info}")
  except: pass
@service
def log_state(entity, expr):
  log_state_factory(entity, expression=expr)

class Logfile:
  def __init__(self, name):
    self.name = name.replace("scripts.", "")
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
        self.logger.debug(message)
        self.logs.append(message)
    elif isinstance(message, list): 
      for msg in message:
        self.log(msg.replace("\n", ""))
      self.log(" ")
    elif message == " ":
        self.logger.debug('\n')
        
  def truncate(self):
    try: service.call("pyscript", "log_truncate", logfile=self.logfile, blocking=True)
    except: pass
  
  def finished(self):
    logs = "\n".join(self.logs)
    log(f"[executed] {self.name}: {logs}")
    return { "service": {self.name}, "logs": logs }