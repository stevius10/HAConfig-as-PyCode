from constants import PATH_LOGS

import logging
import os

class Log:
  
  format = logging.Formatter('%(asctime)s %(funcName)s:%(lineno)d %(message)s')
  
  def __init__(self, name):
    self.name = name.replace("scripts.", "")
    logpath = os.path.join(PATH_LOGS, self.name) + ".log"
    self.logger = logging.getLogger(self.name)
    self.logs = []
    
    handler = logging.handlers.WatchedFileHandler(logpath, mode='w')
    handler.setLevel(logging.INFO)
    handler.setFormatter(format)
    
    self.logger.addHandler(handler)
  
  def log(self, message, ha=False):
    if message: 
      self.logger.info(message)
      self.logs.append(message)
      if ha:
        log.info(message)
  
  def finished(self):
    logs = "\n".join(self.logs)
    self.log(f"[executed] {self.name} ({logs})", ha=True)
    return { "logs":  logs }