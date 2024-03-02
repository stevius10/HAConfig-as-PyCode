from constants import PATH_LOGS

import logging
import os

class Log:

  def __init__(self, logfile):
      self.logfile = logfile
      self.logpath = f"{PATH_LOGS}{logfile}"
      self.__setup()

  def __call__(self, message):
    print(message)
    logging.info(message)

  def __setup(self):
    # if os.path.exists(self.logpath):
      # os.remove(self.logpath)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", handlers=[logging.StreamHandler(), logging.FileHandler(self.logpath)])
