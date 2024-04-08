from config import LOG_SYS_LOGGER, PATH_LOGS

import datetime
import logging
import os
import regex as re

class Logfile:
    
  def __init__(self, name):
    pyscript.log(msg="0")
    self.name = name.replace("scripts.", "")
    self.logger = logging.getLogger(self.name)
    self.logs = []
    self.logfile = os.path.join(PATH_LOGS, self.name) + ".log"

    await service.call("pyscript", "log_truncate", logfile=self.logfile, blocking=True)
    pyscript.log(msg="gg")

    handler = logging.FileHandler(self.logfile, mode='w+')
    handler.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))

    self.logger.addHandler(handler)
    self.logger.setLevel(logging.DEBUG)
    self.logger.propagate = False
    
    self("# {}".format(datetime.datetime.now()))
    
  def __call__(self, message):

    self.append(message=message)
    
  def append(self, message=None):
    pyscript.log(msg="h")
    if isinstance(message, str):
      pyscript.log(msg="2")
      if re.search('[a-zA-Z]', message): 
        self.logger.debug(message)
        self.logs.append(message)
        pyscript.log(msg=logs)
        
    elif isinstance(message, list): 
      for msg in message:
        self.log(msg.replace("\n", ""))
      self.log(" ")
    
    elif message == " ":
        self.logger.debug('\n')

  def finished(self):
    logs = "\n".join(self.logs)
    pyscript.log(msg=f"[executed] {self.name}: {logs}")
    
    return { "service": {self.name}, "logs": logs }