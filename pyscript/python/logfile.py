import json
import logging
import os
from pathlib import Path

from constants.config import CFG_LOGFILE_DEBUG_FILE, CFG_LOGFILE_FORMAT, CFG_LOGFILE_LOG_SIZE, CFG_PATH_DIR_LOG, CFG_PATH_DIR_PY_LOGS_COMPONENTS

os.environ['PYTHONDONTWRITEBYTECODE'] = "1"

class Logfile:
  _logger = None

  def __init__(self, name=None, log_dir=None, timestamp=True):
    self.timestamp = timestamp
    if name:
      self.name = name.split(".")[1] if not name.isalpha() else name
      self.log_dir = log_dir if log_dir else CFG_PATH_DIR_PY_LOGS_COMPONENTS
      self._logger = self._get_file_logger()
    else:
      self.log_dir = log_dir if log_dir else CFG_PATH_DIR_LOG
      self._logger = self._get_debug_logger()

  def _get_file_logger(self):
    self.history = []
    self.logfile = Path(self.log_dir, f"{self.name}.log")
    logger = self._create_logger(self.logfile)
    return logger

  @classmethod
  def _get_debug_logger(cls):
    if cls._logger is None:
      debug_logfile = Path(CFG_PATH_DIR_LOG, f"{CFG_LOGFILE_DEBUG_FILE}.log")
      cls._logger = cls._create_logger(debug_logfile)
    return cls._logger

  @staticmethod
  def _create_logger(logfile):
    logger = logging.getLogger(logfile.stem)
    if logger.hasHandlers():logger.handlers.clear()
    handler = logging.FileHandler(logfile, mode='w+')
    if self.timestamp: handler.setFormatter(logging.Formatter(CFG_LOGFILE_FORMAT))
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

      return { "file": self.logfile.as_posix(), "result": self.history }
    except Exception as e:
      return str(e)