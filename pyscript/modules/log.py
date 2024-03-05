from constants import PATH_LOGS

import logging
import re
import os
import subprocess

from datetime import datetime

class Log:
    
  def __init__(self, name):
    # pyscript.log_truncate(log_file=log_file, size_log_entries=0)
    
    self.name = name.replace("scripts.", "")
    log_file = os.path.join(PATH_LOGS, self.name) + ".log"
    
    self.logs = []
    self.logger = logging.getLogger(self.name)
    self.logger.propagate = False
    self.logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(log_file, mode='w+')
    format = logging.Formatter('%(asctime)s: %(message)s')
    handler.setFormatter(format)
    self.logger.addHandler(handler)
    self.log("# {}".format(datetime.now()))
    
  def log(self, message=None):
    
    if isinstance(message, list): 
      for msg in message:
        self.log(msg.replace("\n", ""))
      self.log(" ")
    
    elif isinstance(message, str):
      if re.search('[a-zA-Z]', message): 
        self.logger.debug(message)
        self.logs.append(message)
        
    elif message == " ":
        self.logger.debug('\n')
        
  def finished(self):
    logs = ("; ".join(filter(None, self.logs))).replace("\n", "")
    log.info(f"[executed] {self.name}: {logs}")
    return { "logs":  logs }