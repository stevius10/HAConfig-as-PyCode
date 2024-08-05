import random
import string

from constants.config import CFG_NOTIFICATION_TARGET_DEFAULT, CFG_NOTIFICATION_ID_LENGTH
from constants.data import DATA_DEVICES

from utils import *

@service
def notify(message, data=None, target=CFG_NOTIFICATION_TARGET_DEFAULT, default=True, interruptable=False, synced=True):
  devices = DATA_DEVICES.get(target) if target else [target for targets in DATA_DEVICES.values() for target in targets]

  if default:
    devices = [device for device in devices if device.get("default")]

  if synced:
    data = data or {}
    data.setdefault('apns_headers', {})['apns-collapse-id'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=CFG_NOTIFICATION_ID_LENGTH))

  if interruptable:
    if not confirmable_notification(message, data, devices):
      return False

  for device in devices:
    service.call("notify", f"mobile_app_{device['id']}", message=message, data=data)

  return True

@debugged
@service
def shortcut(message, shortcut, input=None, target=CFG_NOTIFICATION_TARGET_DEFAULT, interruptable=False, **kwargs):
  data = {"shortcut": {"name": shortcut, "input": input}}

  for key, value in kwargs.items():
    if isinstance(value, str):
      data["shortcut"][key] = value

  if interruptable:
    if not confirmable_notification(message, data, DATA_DEVICES.get(target, [])):
      return False

  notify(message=message, data=data, target=target)
  return True

def confirmable_notification(message, data, devices):
  data.update({'actions': [{'action': 'ABORT', 'title': 'Abbrechen'}, {'action': 'CONTINUE', 'title': 'OK'}]})

  for device in devices:
    service.call("notify", f"mobile_app_{device['id']}", message="lorem ipsum", data=data)

  return wait_for_continue()

async def wait_for_continue():
  for _ in range(10):
    events = await task.wait_until(event_type="mobile_app_notification_action")
    for event in events:
      if event.data['action'] == 'ABORT':
        return False
      if event.data['action'] == 'CONTINUE':
        return True
    await task.sleep(1)
  return True


# import random
# import string

# from constants.config import CFG_NOTIFICATION_TARGET_DEFAULT, CFG_NOTIFICATION_ID_LENGTH
# from constants.data import DATA_DEVICES

# from utils import *

# # Notification

# @logged
# @service
# def notify(message, data=None, target=CFG_NOTIFICATION_TARGET_DEFAULT, default=True, synced=True):
#   devices = DATA_DEVICES.get(target) if target else [target for targets in DATA_DEVICES.values() for target in targets]

#   if default:
#     devices = [device for device in devices if device.get("default")]
    
#   if synced:
#     data = data or {}
#     data.setdefault('apns_headers', {})['apns-collapse-id'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=CFG_NOTIFICATION_ID_LENGTH))

#   for device in devices:
#     service.call("notify", f"mobile_app_{device['id']}", message=message, data=data)

# @debugged
# @service
# def shortcut(message, shortcut, input=None, target=CFG_NOTIFICATION_TARGET_DEFAULT, **kwargs):
  
#   data = { "shortcut": { "name": shortcut, "input": input } }

#   for key, value in kwargs.items():
#     if isinstance(value, str):
#       data["shortcut"][key] = value
  
#   notify(message=message, data=data, target=target)
