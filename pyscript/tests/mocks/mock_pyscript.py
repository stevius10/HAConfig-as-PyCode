from functools import wraps
from unittest.mock import MagicMock

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
    def decorator(*args, **kwargs):
      if 'file' in kwargs:
        del kwargs['file']
      if 'logfile' in kwargs:
        del kwargs['logfile']
      return func(*args, **kwargs)
    return decorator

  @staticmethod
  def time_trigger(func):
    def decorator(*args, **kwargs):
      if 'trigger_type' in kwargs:
        del kwargs['trigger_type']
      return func(*args, **kwargs)
    return decorator

  @staticmethod
  def event_trigger(self, *args, **kwargs):
    def decorator(func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
      return wrapper
    return decorator

  @staticmethod
  def mqtt_trigger(self, *args, **kwargs):
    def decorator(func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
      return wrapper
    return decorator

  @staticmethod
  def state_active(self, *args, **kwargs):
    def decorator(func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
      return wrapper
    return decorator

  @staticmethod
  def time_active(self, *args, **kwargs):
    def decorator(func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
      return wrapper
    return decorator

  @staticmethod
  def task_unique(self, *args, **kwargs):
    def decorator(func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
      return wrapper
    return decorator

pyscript = MockPyscript()
