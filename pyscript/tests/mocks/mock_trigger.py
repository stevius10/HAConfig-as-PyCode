class MockTrigger:
  def __init__(self):
    self.triggers = []

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

  def simulate_trigger(self, trigger_type, *args, **kwargs):
    for t_type, func, t_args, t_kwargs in self.triggers:
        if t_type == trigger_type:
            if all(arg in args for arg in t_args) and all(key in kwargs for key in t_kwargs):
                return func(*args, **kwargs)
    return None