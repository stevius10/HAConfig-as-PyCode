from constants.entities import *

from utils import *

@service
@logged
def script_off(away=False):
  script_off_air()
  script_off_heating(away=away)
  script_off_lights(away=away)
  script_off_media()
  script_off_switches()
  script_off_tv()

@service
def script_off_away():
  script_off(away=True)

@service
def script_off_air(entity=None):
  if entity == None:
    script_off_air(entity=SCRIPT_OFF_ENTITIES_AIR)
  elif isinstance(entity, list):
    for item in entity:
      script_off_air(entity=item)
  elif isinstance(entity, str):
    turn_off(entity=entity)
    
def script_off_heating(entity=None, away=False):
  if entity == None:
    script_off_heating(entity=SCRIPT_OFF_ENTITIES_HEATING, away=away)
  if isinstance(entity, str):
    if not away: 
      climate.turn_off(entity_id=entity)
  if isinstance(entity, list):
    for item in entity:
      script_off_heating(entity=item, away=away)

def script_off_media(entity=None):
  if entity == None:
    script_off_media(entity=SCRIPT_OFF_ENTITIES_MEDIA)
  if isinstance(entity, list):
    for item in entity:
      turn_off(entity=item)

def script_off_lights(entity=None, away=False):
  if entity == None:
    script_off_lights(entity=SCRIPT_OFF_ENTITIES_LIGHT)
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
      
def script_off_switches(entity=None):
  if entity == None:
    script_off_switches(entity=SCRIPT_OFF_ENTITIES_SWITCHES)
  if isinstance(entity, list):
    for item in entity:
      turn_off(entity=item)
      
def script_off_tv(entity=None):
  if entity == None:
    script_off_tv(entity=SCRIPT_OFF_ENTITIES_TV)
  if isinstance(entity, str):
    try: 
      turn_off(entity)
    except Exception: 
      webostv.command(entity_id=entity, command="system/turnOn")
  if isinstance(entity, list):
    for item in entity:
      turn_off(entity=item)
      
# Helper

@service
def turn_off(entity):
  homeassistant.turn_off(entity_id=entity)
