from constants import EVENT_SYSTEM_LOG_TRUNCATED, PATH_LOGS

import logging
import re
import os
import subprocess

from datetime import datetime

class Logfile:
    
  def __init__(self, name):
    self.name = name.replace("scripts.", "")
    self.logger = logging.getLogger(self.name)
    self.logs = []
    self.logfile = os.path.join(PATH_LOGS, self.name) + ".log"
    
    pyscript.ha_log_truncate(logfile=self.logfile)
    task.wait_until(event_trigger=EVENT_SYSTEM_LOG_TRUNCATED, timeout=3)
    
    handler = logging.FileHandler(self.logfile, mode='w+')
    handler.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))

    self.logger.addHandler(handler)
    self.logger.setLevel(logging.DEBUG)
    self.logger.propagate = False
    
    self.log("# {}".format(datetime.now()))
    
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
    log.info(f"[executed] {self.name}: {self.logs}")
    return { "logs":  self.logs }