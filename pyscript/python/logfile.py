import logging
from pathlib import Path

PATH_DIR_PY_LOG = "/config/pyscript/logs/"

LOG_LOGFILE_FORMAT = "%(asctime)s: %(message)s"

class Logfile:
  _logger = None

  def __init__(self, ctx=None):
    self.name = "debug"
    if ctx is not None:
      self._logger = self._get_file_logger(ctx)
    else:
      self._logger = self._get_debug_logger()

  def _get_file_logger(self, ctx):
    self.history = []
    self.name = ctx.split(".")[1]
    logger = self._create_logger(self.name)
    return logger

  @classmethod
  def _get_debug_logger(cls):
    if cls._logger is None:
      cls._logger = cls._create_logger(name=cls.name)
    return cls._logger

  @staticmethod
  def _create_logger(name):
    logfile = Path(PATH_DIR_PY_LOG, f"{name}.log")
    handler = logging.FileHandler(logfile, mode='w+')
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

  @classmethod
  def debug(cls, message=None):
    logger = cls._get_debug_logger()
    if isinstance(message, str):
      if message:
        logger.info(message)
    elif isinstance(message, list):
      for msg in message:
        if msg: logger.info(message)

  def close(self):
    if hasattr(self, 'history'):
      if self.history:
        self.history = "\n".join(str(item) for item in self.history)
        return {"service": self.name, "logs": self.history}
    return {}