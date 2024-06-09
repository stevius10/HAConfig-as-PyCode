import logging
from pathlib import Path

PATH_DIR_PY_LOG = "/config/pyscript/logs/"  # TODO: from constants.config import *

LOG_LOGFILE_FORMAT = "%(asctime)s: %(message)s"

class Logfile:
  def __init__(self, ctx=None):
    if ctx is not None:
      self._logger = self._get_file_logger(ctx)
    else:
      self._logger = self._get_debug_logger()

  def _get_file_logger(self, ctx):
    self.history = []
    logger = self._create_logger(ctx.split(".")[1])
    return logger
  
  def _get_debug_logger(self):
    logger = self._create_logger("debug")
    return logger
  
  def _create_logger(self, name):
    self.name = name
    self.logfile = Path(PATH_DIR_PY_LOG, f"{self.name}.log")
    handler = logging.FileHandler(self.logfile, mode='w+')
    handler.setFormatter(logging.Formatter(LOG_LOGFILE_FORMAT))
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    return logger

  def log(self, message=None):
    if isinstance(message, str):
      if message:
        self._logger.info(message)
        self.history.append(message)
    elif isinstance(message, list):
      for msg in message:
        if msg: self.log(str(msg))

  def close(self):
    if self.history:
      self.history = "\n".join(str(item) for item in self.history)
      return { "service": self.name, "logs": self.history }
    else:
      return {}