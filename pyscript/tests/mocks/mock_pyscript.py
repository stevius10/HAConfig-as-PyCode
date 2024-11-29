import os
import sys

class MockPyscript:
    def __init__(self):
        self.global_vars = {}
        self.triggers = []
        self.services = {}
        self.states = {}
        self.timers = {}
        self.events = []
        self.config = {
            'allow_all_imports': True,
            'hass_is_global': True
        }
        self.setup_environment()

    def setup_environment(self):
        os.environ['HASS_CONFIG'] = '/config'
        pyscript_paths = [
            '/config/pyscript',
            '/config/pyscript/apps',
            '/config/pyscript/modules',
            '/config/pyscript/scripts',
            '/config/pyscript/tests',
            '/config/pyscript/tests/unit',
            '/config/pyscript/tests/integration',
            '/config/pyscript/tests/functional'
        ]
        for path in pyscript_paths:
            if path not in sys.path:
                sys.path.append(path)

    def call_service(self, domain, service, **kwargs):
        if domain in self.services and service in self.services[domain]:
            return self.services[domain][service](**kwargs)
        else:
            raise ValueError(f"Service {domain}.{service} not found")

    def set_state(self, entity_id, state, **kwargs):
        self.states[entity_id] = {'state': state, 'attributes': kwargs}

    def get_state(self, entity_id, attribute=None):
        if entity_id not in self.states:
            return None
        if attribute is None:
            return self.states[entity_id]['state']
        return self.states[entity_id]['attributes'].get(attribute)

    def fire_event(self, event_type, **kwargs):
        self.events.append({'event_type': event_type, 'data': kwargs})

    class MockTask:
        def __init__(self):
            self.tasks = []

        @staticmethod
        def sleep(seconds):
            pass

        @staticmethod
        async def wait_until(*args, **kwargs):
            pass

    @staticmethod
    def task_unique(task_name, kill_me=False):
        def decorator(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def pyscript_executor(func):
        def decorator(func):
            def wrapper():
                return func()
            return wrapper
        return decorator

    @staticmethod
    def service(func):
        def decorator(func):
            def wrapper():
                return func()
            return wrapper
        return decorator

    @staticmethod
    def state_trigger(*args, **kwargs):
        def decorator(func):
            def wrapper(var_name=None, value=None, old_value=None, **kwargs):
                return func(var_name=var_name, value=value, old_value=old_value, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def time_trigger(*args, **kwargs):
        def decorator(func):
            def wrapper(trigger_type="time", **kwargs):
                return func(trigger_type=trigger_type, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def event_trigger(*args, **kwargs):
        def decorator(func):
            def wrapper(trigger_type="event", event_type=None, **kwargs):
                return func(trigger_type=trigger_type, event_type=event_type, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def state_active(*args, **kwargs):
        def decorator(func):
            def wrapper(var_name=None, value=None, old_value=None, **kwargs):
                return func(var_name=var_name, value=value, old_value=old_value, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def time_active(*args, **kwargs):
        def decorator(func):
            def wrapper(trigger_type="time", **kwargs):
                return func(trigger_type=trigger_type, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def event_active(*args, **kwargs):
        def decorator(func):
            def wrapper(trigger_type="event", event_type=None, **kwargs):
                return func(trigger_type=trigger_type, event_type=event_type, **kwargs)
            return wrapper
        return decorator