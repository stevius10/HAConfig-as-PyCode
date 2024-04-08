from config import LOG_SYS_LOGGER, PATH_LOGS

import datetime
import inspect
import logging
import os
import regex as re

class Logs:
  @staticmethod
  def __call__(self, message):
    log.info("2")
    
    _LOGGER = logger.getLogger(LOG_SYS_LOGGER)
    _LOGGER.info("1")
    _LOGGER.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    _LOGGER.addHandler(handler)
    system_log.write(message=message, logger=LOG_SYS_LOGGER, level="error")
    await system_log.write(message=message, level="error")
    
    service.call(domain="system_log", entity="write", message=message)

class Logfile:
    
  def __init__(self, name):
    self.name = name.replace("scripts.", "")
    self.logger = logging.getLogger(self.name)
    self.logs = []
    self.logfile = os.path.join(PATH_LOGS, self.name) + ".log"
    
    service.call("pyscript", "log_truncate", logfile=self.logfile, blocking=True)

    handler = logging.FileHandler(self.logfile, mode='w+')
    handler.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))

    self.logger.addHandler(handler)
    self.logger.setLevel(logging.DEBUG)
    self.logger.propagate = False
    
    self.log("# {}".format(datetime.datetime.now()))
    
  def __call__(self, message):
    log(message=message)
    
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

  def finished(self):
    logs = "\n".join(self.logs)
    Logs(f"[executed] {self.name}: {logs}")
    return { "logs": logs }