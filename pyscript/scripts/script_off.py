from config import AUTO_OFF_AWAY_TRANSITION
from mapping import SCRIPT_AIR_CLEANER_PRESET_MODE_AWAY

ENTITIES_AIR = [
  "humidifier.luftbefeuchter", 
  "fan.wz_luft",
  "fan.sz_luft",
  "fan.sz_ventilator",
  "switch.sz_luftung",
  "switch.wz_ventilator"
]

ENTITIES_HEATING = [
  "clima.wz_heizung",
  "clima.sz_heizung",
  "clima.k_heizung"
]

ENTITIES_MEDIA= [
  "media_player.bad",
  "media_player.kueche",
  "media_player.schlafzimmer",
  "media_player.wohnzimmer",
  "media_player.uberall"
]

ENTITIES_LIGHT = [
  "light.wz_beleuchtung",
  "light.sz_beleuchtung",
  "light.k_beleuchtung",
  "light.g_beleuchtung"
]

ENTITIES_SCRIPTS = [
  "script.gh_luften"
]

ENTITIES_SERVICES = [
  "switch.fritz_box_7530_wi_fi_generation_lockdown_gast"
]

ENTITIES_SWITCHES = [
  "switch.bett",
  "switch.sofa",
  "switch.heizdecke"
]

ENTITIES_TV = [
  "media.wz_fernseher",
  "media.sz_fernseher"
]

@service
def script_off(away=False):
  script_off_air()
  script_off_heating(away=away)
  script_off_lights(away=away)
  script_off_media()
  script_off_scripts()
  script_off_services()
  script_off_switches()
  script_off_tv()

@service
def script_off_away():
  script_off(away=True)

@service
def script_off_air(entity=None):
  if entity == None:
    script_off_air(entity=ENTITIES_AIR)
  elif isinstance(entity, list):
    for item in entity:
      script_off_air(entity=item)
  elif isinstance(entity, str):
    turn_off(entity=entity)
    
@service
def script_off_heating(entity=None, away=False):
  if entity == None:
    script_off_heating(entity=ENTITIES_HEATING, away=away)
  if isinstance(entity, str):
    if not away: 
      climate.turn_off(entity_id=entity)
    else:
      climate.set_preset_mode(entity_id=entity, preset_mode=SCRIPT_AIR_CLEANER_PRESET_MODE_AWAY)
  if isinstance(entity, list):
    for item in entity:
      script_off_heating(entity=item, away=away)

@service
def script_off_media(entity=None):
  if entity == None:
    script_off_media(entity=ENTITIES_MEDIA)
  if isinstance(entity, list):
    for item in entity:
      turn_off(entity=item)

@service
def script_off_lights(entity=None, away=False):
  if entity == None:
    script_off_lights(entity=ENTITIES_LIGHT)
  if isinstance(entity, str):
    if not away: 
      scene.turn_off(entity_id=entity)
    else:
      scene.turn_off(entity, transition=AUTO_OFF_AWAY_TRANSITION)
  if isinstance(entity, list):
    for item in entity[:-1]:
      turn_off(entity=item)
    if away:
      task.sleep(AUTO_CONFIG_OFF_AWAY_TRANSITION)
    turn_off(entity[-1])

@service
def script_off_scripts(entity=None):
  if entity == None:
    script_off_scripts(entity=ENTITIES_SCRIPTS)
  if isinstance(entity, list):
    for item in entity:
      turn_off(entity=item)

@service
def script_off_services(entity=None):
  if entity == None:
    script_off_switches(entity=ENTITIES_SWITCHES)
  if isinstance(entity, list):
    for item in entity:
      turn_off(entity=item)
      
@service
def script_off_switches(entity=None):
  if entity == None:
    script_off_switches(entity=ENTITIES_SWITCHES)
  if isinstance(entity, list):
    for item in entity:
      turn_off(entity=item)
      
@service
def script_off_tv(entity=None):
  if entity == None:
    script_off_tv(entity=ENTITIES_TV)
  if isinstance(entity, str):
    try: 
      turn_off(entity)
      # adb.send_command(entity_id=entity, command="WAKEUP")
    except Exception: 
      webostv.command(entity_id=entity, command="system/turnOn")
  if isinstance(entity, list):
    for item in entity:
      turn_off(entity=item)
      
# Helper

@service
def turn_off(entity):
  homeassistant.turn_off(entity_id=entity)
