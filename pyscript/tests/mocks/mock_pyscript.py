from unittest.mock import MagicMock
from functools import wraps

class MockState:
  pass

class MockService:
  pass

class MockEvent:
  pass

class MockLog:
  pass

class MockTask:
  pass

class MockPyscript:
  def __init__(self):
    self.hass = MagicMock()
    self.state = MockState()
    self.service = MockService()
    self.event = MockEvent()
    self.log = MockLog()
    self.task = MockTask()

  def state_trigger(self, str_expr, state_hold=None, state_hold_false=None, state_check_now=False, kwargs=None, watch=None):
    def decorator(func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
      return wrapper
    return decorator

  def time_trigger(self, time_spec, kwargs=None):
    def decorator(func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
      return wrapper
    return decorator

  def event_trigger(self, event_type, str_expr=None, kwargs=None):
    def decorator(func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
      return wrapper
    return decorator

  def mqtt_trigger(self, topic, str_expr=None, kwargs=None):
    def decorator(func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
      return wrapper
    return decorator

  def state_active(self, str_expr):
    def decorator(func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
      return wrapper
    return decorator

  def time_active(self, time_spec, hold_off=None):
    def decorator(func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
      return wrapper
    return decorator

  def task_unique(self, task_name, kill_me=False):
    def decorator(func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
      return wrapper
    return decorator

  def pyscript_executor(self, func):
    @wraps(func)
    def wrapper(*args, **kwargs):
      return func(*args, **kwargs)
    return wrapper

  def service(self, service_name=None, supports_response="none"):
    def decorator(func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
      return wrapper
    return decorator
