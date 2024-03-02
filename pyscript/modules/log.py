from constants import PATH_LOGS

import logging
import os

class Log:
    def __init__(self, name):
        logpath = os.path.join(PATH_LOGS, name)
        logging.basicConfig(filename=logpath,
                    filemode='w',
                    format='%(asctime)s,%(msecs)d %(name)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)
        self.logger = logging.getLogger(name)
    
    def __call__(self, message):
      if self.logger:
        self.log(message)
    
    def log(self, message):
      if message: 
        self.logger.error(message)