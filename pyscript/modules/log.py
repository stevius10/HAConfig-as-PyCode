from constants import PATH_LOGS

import logging
import os

class Log:
  
  def __init__(self, logfile=pyscript.get_global_ctx()):
    self.logfile = logfile
    self.logpath = os.path.join(PATH_LOGS, logfile)
    
    logging.basicConfig(filename=self.logpath,
                    filemode='w',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)
    self.logger = logging.getLogger(self.logfile)

  def __call__(self, message):
    self.log(message)
  
  def log(self, message):
    if not message: 
      message = ""
    self.logger.info(message)