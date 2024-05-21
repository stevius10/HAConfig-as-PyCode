from config import *
from entities import AUTO_NOTIFY_ENTITIES
from mapping import NOTIFICATION_ID_CHANGE_DETECTION
from utils import *

from homeassistant.const import EVENT_CALL_SERVICE

import random

entities = AUTO_NOTIFY_ENTITIES
notification_id_change_detection = NOTIFICATION_ID_CHANGE_DETECTION

@state_trigger(expr([str(key) for key in list(entities.keys())]))
def notify_immo(**kwargs):
  if(kwargs.get("old_value") not in STATES_HA_UNDEFINED):
    notify.mobile_app_iphone(
      message="", #kwargs.get("var_name"), 
      data={
        "shortcut": {
          "name": "Notification-Monitor",
          "input": entities[kwargs.get("var_name")],
          "ignore_result": "ignore"
        }
      }
    )

@time_active(EXPR_TIME_ACTIVE)
@time_trigger(EXPR_TIME_UPDATE_SENSORS)
def update_sensors(): 
  task.sleep(random.randint(10, 600))
  for entity in entities:
    homeassistant.update_entity(entity_id=entity)

@event_trigger(EVENT_CALL_SERVICE, "domain == 'persistent_notification' and service == 'create'")
@log_context
def notify_persistent_notification(ns=None, ctx=None, **kwargs):
  service_data=kwargs.get("service_data")
  if service_data.get("notification_id") == notification_id_change_detection:
    notification_data = dict(actions=[dict(action="URI", title=service_data.get("message"), uri=service_data.get("title"))])
    notify.mobile_app_iphone(message=kwargs.get("service_data").get("message"), data=notification_data)
    persistent_notification.dismiss(notification_id=service_data.get("notification_id"))
    log(f"change detected", ns, ctx, service_data.get("title"))