from functools import wraps
from unittest.mock import MagicMock

# Objects
class MockState:
  def __init__(self):
    print("Initializing MockState")
    self.get = MagicMock()
    self.set = MagicMock()
    self.delete = MagicMock()
    self.getattr = MagicMock()
    self.names = MagicMock()
    self.persist = MagicMock()
    self.setattr = MagicMock()

class MockService:
  def __init__(self):
    print("Initializing MockService")
    self.call = MagicMock()
    self.has_service = MagicMock()

class MockEvent:
  def __init__(self):
    print("Initializing MockEvent")
    self.fire = MagicMock()

class MockLog:
  def __init__(self):
    print("Initializing MockLog")
    self.debug = MagicMock()
    self.info = MagicMock()
    self.warning = MagicMock()
    self.error = MagicMock()
    self.print = MagicMock()

class MockTask:
  def __init__(self):
    print("Initializing MockTask")
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

# Mock
class MockPyscript:
  def __init__(self):
    print("Instantiating MockState in MockPyscript")
    self.state = MockState()
    print("Instantiating MockService in MockPyscript")
    self.service = MockService()
    print("Instantiating MockEvent in MockPyscript")
    self.event = MockEvent()
    print("Instantiating MockLog in MockPyscript")
    self.log = MockLog()
    print("Instantiating MockTask in MockPyscript")
    self.task = MockTask()

  # Decorators
  def service(self, service_name=None, supports_response=None):
    print(f"Creating service decorator for {service_name}")
    def decorator(func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        print(f"Executing service decorator for {service_name} with args: {args}, kwargs: {kwargs}")
        return func(*args, **kwargs)
      return wrapper
    return decorator

  def time_trigger(self, time_spec):
    print(f"Creating time_trigger for {time_spec}")
    def decorator(func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        print(f"Executing time_trigger for {time_spec} with args: {args}, kwargs: {kwargs}")
        return func(*args, **kwargs)
      return wrapper
    return decorator

  def event_trigger(self, event_type, str_expr=None, kwargs=None):
    print(f"Creating event_trigger for {event_type}")
    if kwargs is None:
      kwargs = {}
    def decorator(func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        print(f"Executing event_trigger for {event_type} with args: {args}, kwargs: {kwargs}")
        return func(*args, **kwargs)
      return wrapper
    return decorator

  def mqtt_trigger(self, topic, str_expr=None, kwargs=None):
    print(f"Creating mqtt_trigger for {topic}")
    if kwargs is None:
      kwargs = {}
    def decorator(func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        print(f"Executing mqtt_trigger for {topic} with args: {args}, kwargs: {kwargs}")
        return func(*args, **kwargs)
      return wrapper
    return decorator

  # Conditions
  def state_active(self, str_expr):
    print(f"Creating state_active for {str_expr}")
    def decorator(func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        print(f"Executing state_active for {str_expr} with args: {args}, kwargs: {kwargs}")
        return func(*args, **kwargs)
      return wrapper
    return decorator

  def time_active(self, time_spec, hold_off=None):
    print(f"Creating time_active for {time_spec}")
    def decorator(func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        print(f"Executing time_active for {time_spec} with args: {args}, kwargs: {kwargs}")
        return func(*args, **kwargs)
      return wrapper
    return decorator

# Assign the mock to the name `pyscript` to simulate the runtime environment
pyscript = MockPyscript()
