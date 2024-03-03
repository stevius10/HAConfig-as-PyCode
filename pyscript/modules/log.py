from constants import PATH_LOGS

import logging
import re
import os

import subprocess

class Log:
  
  format = logging.Formatter('%(asctime)s: %(message)s')
  
  def __init__(self, name):
    self.name = name.replace("scripts.", "")
    logpath = os.path.join(PATH_LOGS, self.name) + ".log"
    
    pyscript.ha_logs_truncate(logpath=logpath)

    self.logs = []
    self.logger = logging.getLogger(self.name)
    self.logger.propagate = False
    self.logger.setLevel(logging.DEBUG)
    self.logger.addHandler(logging.FileHandler(logpath, mode='w'))
    
  def log(self, message=None):
    
    if isinstance(message, list): 
      for msg in message:
        self.log(msg.replace("\n", ""))
      self.log(" ")
    
    if isinstance(message, str):
      if re.search('[a-zA-Z]', message): 
        self.logger.debug(message)
        self.logs.append(message)
        
    if message == " ":
        self.logger.debug('\n')
        
  def finished(self):
    logs = ("; ".join(filter(None, self.logs))).replace("\n", "")
    log.info(f"[executed] {self.name}: {logs}")
    return { "logs":  logs }