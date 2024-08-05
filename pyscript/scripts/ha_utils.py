import random
import string

from constants.config import CFG_NOTIFICATION_TARGET_DEFAULT, CFG_NOTIFICATION_ID_LENGTH
from constants.data import DATA_DEVICES

from utils import *

# Notification

@logged
@service
def notify(message, data=None, target=CFG_NOTIFICATION_TARGET_DEFAULT, default=True, synced=True):
  devices = DATA_DEVICES.get(target) if target else [target for targets in DATA_DEVICES.values() for target in targets]

  if default:
    devices = [device for device in devices if device.get("default")]
    
  if synced:
    data = data or {}
    data.setdefault('apns_headers', {})['apns-collapse-id'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=CFG_NOTIFICATION_ID_LENGTH))

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
