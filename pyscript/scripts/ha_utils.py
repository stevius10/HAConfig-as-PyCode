from constants import *

default_notification_target = DEFAULT_NOTIFICATION_TARGET

@service
def notify(message, data=None, target=default_notification_target, default=True):
  devices = DEVICES.get(target) if target else [target for targets in DEVICES.values() for target in targets]

  if default:
    devices = [device for device in devices if device.get("default")]

  for device in devices:
    service.call("notify", f"mobile_app_{device['id']}", message=message, data=data)
    
@service
def shortcut(message, shortcut, input=None, target=default_notification_target, **kwargs):

  data = { "shortcut": { "name": shortcut, "input": input } }

  for key, value in kwargs.items():
    if isinstance(value, str):
      data["shortcut"][key] = value
  
  notify(message=message, data=data, target=target)