from constants.expressions import *

from utils import *

import json
import mqttapi as mqtt

AWTRIX_TOPIC = "awtrix/custom/depature"

trigger = []

def mqtt_awtrix_transport_factory(entity): 
  
  @logged
  def mqtt_awtrix_transport(entity=entity, ns=None, ctx=None):
    result = service.call(entity.split(".")[0], entity.split(".")[1])

  trigger.append(mqtt_awtrix_transport)

def mqtt_awtrix_transport_update_railway():
def mqtt_awtrix_transport_update_subway():
def mqtt_awtrix_transport_update_tram():
def mqtt_awtrix_transport_update_bus():

    ubahn_abfahrt = state.get("sensor.ubahn_naechste_abfahrt")
    
    payload = {
        "text": f"S: {sbahn_abfahrt} U: {ubahn_abfahrt}", 
        "icon": 59,
        "color": [255,255,255]
    }
    
    mqtt.publish(AWTRIX_TOPIC, json.dumps(payload))