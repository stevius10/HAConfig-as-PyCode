from functools import wraps
from unittest.mock import MagicMock

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

class MockPyscript:
  def __init__(self):
    self.state = MockState()
    self.event = MockEvent()
    self.log = MockLog()
    self.task = MockTask()

  def service(self, *args, **kwargs):
    def decorator(func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
      return wrapper
    return decorator

  def time_trigger(self, *args, **kwargs):
    def decorator(func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
      return wrapper
    return decorator

  def event_trigger(self, *args, **kwargs):
    def decorator(func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
      return wrapper
    return decorator

  def mqtt_trigger(self, *args, **kwargs):
    def decorator(func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
      return wrapper
    return decorator

  def state_active(self, *args, **kwargs):
    def decorator(func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
      return wrapper
    return decorator

  def time_active(self, *args, **kwargs):
    def decorator(func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
      return wrapper
    return decorator

  def task_unique(self, *args, **kwargs):
    def decorator(func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
      return wrapper
    return decorator

pyscript = MockPyscript()
