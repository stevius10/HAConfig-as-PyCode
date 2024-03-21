from config import PATH_LOGS

import logging
import inspect
import os
import datetime
import regex as re

class Logger:
  def __init__(self):
    pass
  
  def __call__(self, message):
    try:
      current_frame = inspect.currentframe()
      caller_frame = inspect.getouterframes(current_frame)[1]
      function_name = caller_frame.function
      filename = os.path.basename(caller_frame.filename)
      current_time = datetime.datetime.now().strftime("%H:%M")

      logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

      log.info(f"{current_time} - {function_name} in {filename}: {message}")

      print(f"{current_time} - {function_name} in {filename}: {message}")
    except Exception as e:
      print(f"{e}")

class Logfile:
    
  def __init__(self, name):
    self.name = name.replace("scripts.", "")
    self.logger = logging.getLogger(self.name)
    self.logs = []
    self.logfile = os.path.join(PATH_LOGS, self.name) + ".log"
    
    service.call("pyscript", "log_truncate", logfile=self.logfile, blocking=True)

    handler = logging.FileHandler(self.logfile, mode='w+')
    handler.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))

    self.logger.addHandler(handler)
    self.logger.setLevel(logging.DEBUG)
    self.logger.propagate = False
    
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

  def finished(self):
    logs = "\n".join(self.logs)
    log.info(f"[executed] {self.name}: {logs}")
    return { "logs": logs }