import asyncio

class MockPyscript:
  def __init__(self):
    self.global_vars = {}
    self.triggers = []
    self.services = {}
    self.tasks = []
    self.states = {}
    self.timers = {}
    self.events = []

  def set_global_var(self, name, value):
    self.global_vars[name] = value

  def get_global_var(self, name):
    return self.global_vars.get(name)

  def trigger(self, trigger_type, **kwargs):
    self.triggers.append({
      'type': trigger_type,
      'kwargs': kwargs
    })

  def register_service(self, domain, service, func):
    if domain not in self.services:
      self.services[domain] = {}
    self.services[domain][service] = func

  def call_service(self, domain, service, **kwargs):
    if domain in self.services and service in self.services[domain]:
      return self.services[domain][service](**kwargs)
    else:
      raise ValueError(f"Service {domain}.{service} not found")

  def task_create(self, func, *args, **kwargs):
    task = MockTask(func, *args, **kwargs)
    self.tasks.append(task)
    return task

  def log(self, message, level="INFO"):
    print(f"[{level}] {message}")

  def state_trigger(self, *args, **kwargs):
    def decorator(func):
      self.triggers.append(('state_trigger', func, args, kwargs))
      return func
    return decorator

  def time_trigger(self, *args, **kwargs):
    def decorator(func):
      self.triggers.append(('time_trigger', func, args, kwargs))
      return func
    return decorator

  def event_trigger(self, *args, **kwargs):
    def decorator(func):
      self.triggers.append(('event_trigger', func, args, kwargs))
      return func
    return decorator

  def state_active(self, *args, **kwargs):
    def decorator(func):
      self.triggers.append(('state_active', func, args, kwargs))
      return func
    return decorator

  def time_active(self, *args, **kwargs):
    def decorator(func):
      self.triggers.append('time_active', func)