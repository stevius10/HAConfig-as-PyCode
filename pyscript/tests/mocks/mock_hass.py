class MockHass:
  def __init__(self):
    self.states = {}
    self.services = {}
    self.events = []
    self.timers = {}

  def get_state(self, entity_id):
    return self.states.get(entity_id, {}).get('state')

  def get_attributes(self, entity_id):
    return self.states.get(entity_id, {}).get('attributes', {})

  def set_state(self, entity_id, new_state, attributes=None):
    self.states[entity_id] = {
      'state': new_state,
      'attributes': attributes or {}
    }

  def call_service(self, domain, service, **kwargs):
    if domain not in self.services:
      self.services[domain] = {}
    if service not in self.services[domain]:
      self.services[domain][service] = []
    self.services[domain][service].append(kwargs)

  def fire_event(self, event_type, event_data=None):
    self.events.append({
      'event_type': event_type,
      'event_data': event_data or {}
    })

  def start_timer(self, entity_id, duration):
    self.timers[entity_id] = {'duration': duration, 'state': 'active'}

  def cancel_timer(self, entity_id):
    if entity_id in self.timers:
      self.timers[entity_id]['state'] = 'idle'

  def get_timer_state(self, entity_id):
    return self.timers.get(entity_id, {}).get('state', 'idle')

class MockState:
  def __init__(self, entity_id, state, attributes=None):
    self.entity_id = entity_id
    self.state = state
    self.attributes = attributes or {}

class MockServiceCall:
  def __init__(self, domain, service, data=None):
    self.domain = domain
    self.service = service
    self.data = data or {}

class MockEvent:
  def __init__(self, event_type, data=None):
    self.event_type = event_type
    self.data = data or {}