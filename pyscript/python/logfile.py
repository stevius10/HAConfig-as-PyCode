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
        total_lines = len(self.history)
        if total_lines > CFG_LOGFILE_LOG_SIZE:
          half_max_lines = (CFG_LOGFILE_LOG_SIZE - 1) // 2
          self.history = (
            self.history[:half_max_lines] +
            [f"... [{total_lines - 2 * half_max_lines} Zeilen gekürzt] ..."] +
            self.history[-half_max_lines:]
          )
        else:
          self.history = ", ".join(self.history)
    except Exception as e:
      print(f"Error: {e}")
        
'''
  def close(self):
    if hasattr(self, 'history'):
      self.history = ", ".join([str(item) for item in self.history]) if self.history else ""
    else: 
      self.history = ""
    return { "file": self.logfile.as_posix(), "result": self.history[:CFG_LOGFILE_LOG_SIZE]}
'''