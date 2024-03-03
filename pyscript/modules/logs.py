from constants import PATH_LOGS

import logging
import os

class Logs:
  
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

  def __call__(self, message):
    # if self.logger:
      self.log(message)
  
  def log(self, message):
    if message: 
      self.logger.info(message)
      self.logs.append(message)
  
  def info(self, message):
    log.info(message)
    self.log(message)
  
  def finished(self):
    self.info(f"[executed] {self.name} ({self.logs}")
    return { "logs": self.logs }