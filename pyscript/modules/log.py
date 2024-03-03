from constants import PATH_LOGS

import logging
import os

import subprocess

class Log:
  
  format = logging.Formatter('%(asctime)s %(funcName)s:%(lineno)d %(message)s')
  
  def __init__(self, name):
    self.name = name.replace("scripts.", "")
    logpath = os.path.join(PATH_LOGS, self.name) + ".log"
    self.logs = []
    self.logger = logging.getLogger(self.name)
    self.logger.setLevel(logging.INFO)
    handler = logging.handlers.WatchedFileHandler(logpath, mode='w')
    handler.setLevel(logging.INFO)
    handler.setFormatter(format)
    stream = logging.StreamHandler()
    stream.setLevel(logging.INFO)
    stream.setFormatter(format)
    
    self.logger.addHandler(handler)
    #self.logger.addHandler(stream)

  def log(self, message, ha=False):
    
    if isinstance(message, dict): 
      for msg in message.values():
       for k, v in msg.items():
         self.log(v) 
    
    if isinstance(message, list): 
      self.log("".join(message))
    
    if isinstance(message, str):
      self.logger.info(message)
      self.logs.append(message)
      #if ha:
        #log.info(message)
  
  def finished(self):
    logs = (", ".join(self.logs)).replace("\n", "")
    self.log(f"[executed] {self.name}: {logs}")
    return { "logs":  logs }