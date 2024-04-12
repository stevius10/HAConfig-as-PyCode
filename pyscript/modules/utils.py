from config import LOG_SYS_LOGGER, PATH_LOGS

import datetime
import functools
import logging
import os
import regex as re

def log(msg, level="info", logger=LOG_SYS_LOGGER):
  if not isinstance(msg, str): 
    msg = msg.get_name()
    try: pyscript.log(msg=msg, logger=logger, level=level)
    except: pass

def log_func(func):
  def wrapper(*args, **kwargs):
    func_name = func if isinstance(func, str) else func.get_name()
    if "context" in kwargs:
      del kwargs["context"]
    arguments = f"{args}[{kwargs}])"
    log(f"{func_name}{arguments}")
    return func(*args, **kwargs)
  return wrapper

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
    
    await self.log_truncate()
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

  def log_truncate(self):
    try: service.call("pyscript", "log_truncate", logfile=self.logfile, blocking=True)
    except: pass

  def finished(self):
    logs = "\n".join(self.logs)
    log(f"[executed] {self.name}: {logs}")
    
    return { "service": {self.name}, "logs": logs }