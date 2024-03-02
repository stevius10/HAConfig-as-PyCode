from constants import PATH_LOGS

import logging
import os

class Log:
    def __init__(self, name):
        logpath = os.path.join(PATH_LOGS, name) + ".log"
        self.logger = logging.getLogger(name)
        self.logger.addHandler(logging.FileHandler(logpath, mode='w'))
        self.logger.addHandler(logging.handlers.WatchedFileHandler(logpath, mode='w'))

    def __call__(self, message):
      if self.logger:
        self.log(message)
    
    def log(self, message):
      if message: 
        self.logger.info(message)
        logging.info(message)
      