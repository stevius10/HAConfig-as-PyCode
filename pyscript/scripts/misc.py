# TODO: Refactor

from constants import *
from mapping import NOTIFICATION_ID_CHANGE_DETECTION

from homeassistant.const import EVENT_CALL_SERVICE

notification_id_change_detection = NOTIFICATION_ID_CHANGE_DETECTION

@event_trigger(EVENT_CALL_SERVICE, "domain == 'persistent_notification' and service == 'create'")
def notify_persistent_notification(ns=None, ctx=None, **kwargs):
  service_data = kwargs.get("service_data")
  if service_data.get("notification_id") == notification_id_change_detection:
    notification_data = dict(actions=[
      dict(action="URI", title=service_data.get("message"), uri=service_data.get("title"))
    ])
    notify(
      message=service_data.get("message"),
      data=notification_data,
      device_type="mobile"
    )
    persistent_notification.dismiss(notification_id=service_data.get("notification_id"))