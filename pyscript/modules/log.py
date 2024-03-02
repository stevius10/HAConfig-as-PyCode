from constants import PATH_LOGS

import logging
import os

class Log:
    def __init__(self, logfile=pyscript.get_global_ctx()):
        self.logfile = os.path.join(PATH_LOGS, logfile)
        self.__setup()

    def __call__(self, message):
        self.log(self, message)
    
    def log(self, message):
      log.info(message)

    def __setup(self):
      os.remove(self.logfile)
      logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", handlers=[logging.StreamHandler(), logging.FileHandler(self.logfile)], force=True)