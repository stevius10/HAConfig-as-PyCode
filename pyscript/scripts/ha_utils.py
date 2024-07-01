from constants.config import *
from constants.mappings import *

from utils import *

@logged
@service
def notify(message, data=None, target=DEFAULT_NOTIFICATION_TARGET, default=True):
  devices = DEVICES.get(target) if target else [target for targets in DEVICES.values() for target in targets]

  if default:
    devices = [device for device in devices if device.get("default")]

  for device in devices:
    service.call("notify", f"mobile_app_{device['id']}", message=message, data=data)

@debugged
@service
def shortcut(message, shortcut, input=None, target=DEFAULT_NOTIFICATION_TARGET, **kwargs):
  
  data = { "shortcut": { "name": shortcut, "input": input } }

  for key, value in kwargs.items():
    if isinstance(value, str):
      data["shortcut"][key] = value
  
  notify(message=message, data=data, target=target)