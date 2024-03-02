from constants import PATH_LOGS

import logging
import os

class Log:
    def __init__(self, logfile=pyscript.get_global_ctx()):
        self.logfile = os.path.join(PATH_LOGS, logfile)
        self.__setup()

    def __call__(self, message):
        log(self, message)
    
    def log(self, message):
      print(message)
      logging.info(message)
      log.info(message)

    def __setup(self):
      logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", handlers=[logging.StreamHandler(), logging.FileHandler(self.logfile)], force=True)

