from functools import wraps
from unittest.mock import MagicMock
from utils import *

class MockPyscript:

  class MockState:
    def __init__(self):
      self.get = MagicMock()
      self.set = MagicMock()
      self.delete = MagicMock()
      self.getattr = MagicMock()
      self.names = MagicMock()
      self.persist = MagicMock()
      self.setattr = MagicMock()

  class MockEvent:
    def __init__(self):
      self.fire = MagicMock()

  class MockLog:
    def __init__(self):
      self.debug = MagicMock()
      self.info = MagicMock()
      self.warning = MagicMock()
      self.error = MagicMock()
      self.print = MagicMock()

  class MockTask:
    def __init__(self):
      self.create = MagicMock()
      self.cancel = MagicMock()
      self.current_task = MagicMock()
      self.name2id = MagicMock()
      self.wait = MagicMock()
      self.add_done_callback = MagicMock()
      self.remove_done_callback = MagicMock()
      self.executor = MagicMock()
      self.sleep = MagicMock()
      self.unique = MagicMock()
      self.wait_until = MagicMock()

  def __init__(self):
    self.state = self.MockState()
    self.event = self.MockEvent()
    self.log = self.MockLog()
    self.task = self.MockTask()

  @staticmethod
  def service(func):
    @wraps(func)
    def decorator(*args, **kwargs):
      kwargs.pop('file', None)
      kwargs.pop('logfile', None)
      return func(*args, **kwargs)
    return decorator

  @staticmethod
  def time_trigger(func):
    @wraps(func)
    def decorator(*args, **kwargs):
      kwargs.pop('trigger_type', None)
      return func(*args, **kwargs)
    return decorator

  @staticmethod
  def event_trigger(func, **kwargs):
    @wraps(func)
    def wrapper(*args, **kwargs):
      result = func(*args, **kwargs)
      return result
    return wrapper

  @staticmethod
  def state_active(func):
    @wraps(func)
    def decorator(*args, **kwargs):
      return func(*args, **kwargs)
    return decorator

  @staticmethod
  def time_active(func):
    @wraps(func)
    def decorator(*args, **kwargs):
      return func(*args, **kwargs)
    return decorator

  @staticmethod
  def task_unique(*args, **kwargs):
    def decorator(func):
      def wrapper(*func_args, **func_kwargs):
        print(func)
        log(func)
        return func(*func_args, **func_kwargs)
      return wrapper
    return decorator