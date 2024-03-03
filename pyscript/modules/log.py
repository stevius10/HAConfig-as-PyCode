from constants import PATH_LOGS

import logging
import os

import subprocess

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
    
    if isinstance(message, dict): 
      for msg in message.values():
       for k, v in msg.items():
         self.log(v) 
    
    if isinstance(message, list): 
      self.log("\n".join(message))
    
    if isinstance(message, str):
      self.logger.info(message)
      self.logs.append(message)
      if ha:
        log.info(message)
  
  def finished(self):
    logs = ("".join(self.logs)).replace("\n", "")
    self.log(f"[executed] {self.name}: {logs}", ha=True)
    return { "logs":  logs }