from config import LOG_SYS_LOGGER, PATH_LOGS

import datetime
import logging
import os
import regex as re

class Logfile:
    
  def __init__(self, name):
    self.name = name.replace("scripts.", "")
    self.logger = logging.getLogger(self.name)
    self.logs = []
    self.logfile = os.path.join(PATH_LOGS, self.name) + ".log"

    # pyscript.log_truncate(logfile=self.logfile)

    handler = logging.FileHandler(self.logfile, mode='w+')
    handler.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))

    self.logger.addHandler(handler)
    self.logger.setLevel(logging.DEBUG)
    self.logger.propagate = False
    
    await self.log_truncate()
    self.log("# {}".format(datetime.datetime.now()))
    
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

  async def log_truncate(self):
    if "pyscript" in globals() is not None: 
      await service.call(domain="pyscript", name="log_truncate", logfile=self.logfile, blocking=True)
    # service.call(domain=func.split(".")[0], name=func.split(".")[1], logfile=self.logfile, blocking=True)

  def finished(self):
    logs = "\n".join(self.logs)
    pyscript.log(msg=f"[executed] {self.name}: {logs}")
    
    return { "service": {self.name}, "logs": logs }