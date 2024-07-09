import logging
import os
from pathlib import Path
import sys

from constants.config import CFG_LOGFILE_DEBUG_FILE, CFG_LOGFILE_FORMAT, CFG_LOGFILE_LOG_SIZE, CFG_PATH_DIR_LOG

os.environ['PYTHONDONTWRITEBYTECODE'] = "1"

class Logfile:
  _logger = None

  def __init__(self, name=None):
    if name:
      self.name = name.split(".")[1] if not name.isalpha() else name
      self._logger = self._get_file_logger()
    else:
      self._logger = self._get_debug_logger()

  def _get_file_logger(self):
    self.history = []
    self.logfile = Path(CFG_PATH_DIR_LOG, f"{self.name}.log")
    logger = self._create_logger(name=self.name)
    return logger

  @classmethod
  def _get_debug_logger(cls):
    if cls._logger is None:
      cls._logger = cls._create_logger(name=CFG_LOGFILE_DEBUG_FILE)
    return cls._logger

  @staticmethod
  def _create_logger(name):
    logfile = Path(CFG_PATH_DIR_LOG, f"{name}.log")
    logger = logging.getLogger(name)
    if logger.hasHandlers():
      logger.handlers.clear()
    handler = logging.FileHandler(logfile, mode='w+')
    handler.setFormatter(logging.Formatter(CFG_LOGFILE_FORMAT))
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    return logger

  def log(self, message=None):
    if message: 
      if isinstance(message, str):
        self._logger.info(message)
        self.history.append(message)
      elif isinstance(message, list):
        for msg in message:
          self.log(msg)

  @classmethod
  def debug(cls, message=None):
    if message: 
      if isinstance(message, str):
        cls._get_debug_logger().info(message)
      elif isinstance(message, list):
        for msg in message:
          cls.debug(msg)

  def close(self):
    try:
      if hasattr(self, 'history'):
        total_chars = sum(len(item) for item in self.history)
        if total_chars > CFG_LOGFILE_LOG_SIZE:
          half_max_chars = (CFG_LOGFILE_LOG_SIZE - len("... [Zeichen gekürzt] ...")) // 2
          start_part, end_part = [], []
          start_length, end_length = 0, 0
  
          for item in self.history:
            if start_length + len(item) < half_max_chars:
              start_part.append(item)
              start_length += len(item)
            else:
              break
  
          for item in reversed(self.history):
            if end_length + len(item) < half_max_chars:
              end_part.append(item)
              end_length += len(item)
            else:
              break
  
          removed_chars = total_chars - start_length - end_length
          self.history = start_part + [f"... [{removed_chars} Zeichen gekürzt] ..."] + list(reversed(end_part))
        else:
          self.history = ", ".join(self.history)
      else:
        self.history = ""
      return {"file": Path(CFG_PATH_DIR_LOG, f"{self.name}.log").as_posix(), "result": self.history}
    except Exception as e:
      return {"error": str(e)}

'''
  def close(self):
    if hasattr(self, 'history'):
      self.history = ", ".join([str(item) for item in self.history]) if self.history else ""
    else: 
      self.history = ""
    return { "file": self.logfile.as_posix(), "result": self.history[:CFG_LOGFILE_LOG_SIZE]}
'''