from constants import PATH_LOGS

import logging
import os

class Logs:
  
  format = logging.Formatter('%(asctime)s %(funcName)s:%(lineno)d %(message)s')
  
  def __init__(self, name):
    self.name = name.replace("scripts.", "")
    logpath = os.path.join(PATH_LOGS, self.name) + ".log"
    self.logger = logging.getLogger(self.name)
    
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
  
  def finished(logs):
    logs.log(f"[executed] {self.name} ({logs}")
    return logs