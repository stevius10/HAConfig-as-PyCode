from constants.config import CFG_NOTIFICATION_TARGET_DEFAULT
from constants.data import DATA_DEVICES

from utils import *

# Notification

@logged
@service
def notify(message, data=None, target=CFG_NOTIFICATION_TARGET_DEFAULT, default=True):
  devices = DATA_DEVICES.get(target) if target else [target for targets in DATA_DEVICES.values() for target in targets]

  if default:
    devices = [device for device in devices if device.get("default")]

  for device in devices:
    service.call("notify", f"mobile_app_{device['id']}", message=message, data=data)

@debugged
@service
def shortcut(message, shortcut, input=None, target=CFG_NOTIFICATION_TARGET_DEFAULT, **kwargs):
  
  data = { "shortcut": { "name": shortcut, "input": input } }

  for key, value in kwargs.items():
    if isinstance(value, str):
      data["shortcut"][key] = value
  
  notify(message=message, data=data, target=target)

# Persistence

@logged
@service
def persistence(entity, value=None, default="", result=True, **kwargs): 

  if not value: # store and restore persistence
    state.persist(entity, default)
  else: # set persistence
    if value: 
      state.set(entity, value)
      state.persist(entity)
    if hasattr(kwargs, "attributes"):
      attributes = kwargs['attributes']
      if isinstance(attributes, dict):
        for attribute in attributes:
          state.set(f"{entity}.{attribute}", attributes.get(attribute))
          
    state.persist(entity)
  if result: 
    homeassistant.update_entity(entity_id=entity) # avoid on shutdown 

    return str(state.get(entity))

  else: 
    return ""