from constants import *

default_notification_target = DEFAULT_NOTIFICATION_TARGET

@service
def notify(message, data={}, target=default_notification_target, default=True):
  devices = DEVICES.get(target) if target else [d for dt in DEVICES.values() for d in dt]

  if default:
    devices = [device for device in devices if device.get("default")]

  for device in devices:
    service.call("notify", f"mobile_app_{device['id']}", message=message, data=data)

@service
def shortcut(device_id, message, shortcut, **kwargs):
  data = {"message": message, "data": {"shortcut": {"name": shortcut}}}
  for key, value in kwargs.items():
    if isinstance(value, str):
      data["data"]["shortcut"][key] = value
  notify(message, data, device=device_id)