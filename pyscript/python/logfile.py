import json
import logging
import os
import sys
from pathlib import Path

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
        if '\n' in message:
          for msg in message.split('\n'):
            self.log(msg)
        else:
          self._logger.info(message)
          self.history.append(message)
      elif isinstance(message, list):
        for msg in message:
          self.log(msg)

  @classmethod
  def debug(cls, message=None):
    if message:
      if isinstance(message, str):
        if '\n' in message:
          for msg in message.split('\n'):
            cls.debug(msg)
        else:
          cls._get_debug_logger().info(message)
      elif isinstance(message, list):
        for msg in message:
          cls.debug(msg)
          
  def close(self):
    try:
      if hasattr(self, 'history'):
        lines = len(self.history)
        if lines > CFG_LOGFILE_LOG_SIZE:
          lines_half = CFG_LOGFILE_LOG_SIZE // 2
          lines_half_start = self.history[:lines_half]
          lines_half_stop = self.history[-lines_half:]
          self.history = lines_half_start + [f"... [{lines - len(lines_half_start) - len(lines_half_stop)} lines] ..."] + lines_half_stop
        self.history = " ".join(self.history)

      return { "file": Path(CFG_PATH_DIR_LOG, f"{self.name}.log").as_posix(), "result": self.history }
    except Exception as e:
      return str(e)