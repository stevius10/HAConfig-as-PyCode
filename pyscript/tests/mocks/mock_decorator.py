# TODO

from functools import wraps

class MockDecorator:
  def __init__(self):
    self.services = {}
    self.compiled_functions = set()

  def service(self, service_name=None, supports_response="none"):
    def decorator(func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if supports_response in ["only", "optional"]:
          return result
        return None
      
      nonlocal service_name
      if service_name is None:
        service_name = f"{func.__name__}"
      
      self.services[service_name] = {
        'function': wrapper,
        'supports_response': supports_response
      }
      return wrapper
    return decorator

mock_decorator = MockDecorator()

def service(*args, **kwargs):
  return mock_decorator.service(*args, **kwargs)