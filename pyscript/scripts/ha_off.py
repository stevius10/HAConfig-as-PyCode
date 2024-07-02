from constants.entities import *

from utils import *

@service
@logged
def turnoff(away=False):
  turnoff_air()
  turnoff_heating(away=away)
  turnoff_lights(away=away)
  turnoff_media()
  turnoff_switches()
  turnoff_tv()

@service
def turnoff_away():
  turnoff(away=True)

@service # air management service
def turnoff_air(entity=None):
  if not entity:
    turnoff_air(entity=CLUSTER_ENTITIES_AIR)
  elif isinstance(entity, list):
    for item in entity:
      turnoff_air(entity=item)
  elif isinstance(entity, str):
    turn_off(entity=entity)
    
def turnoff_heating(entity=None, away=False):
  if not entity:
    turnoff_heating(entity=CLUSTER_ENTITIES_HEATING, away=away)
  if isinstance(entity, str):
    if not away: 
      climate.air_control_turn_off(entity_id=entity)
  if isinstance(entity, list):
    for item in entity:
      turnoff_heating(entity=item, away=away)

def turnoff_media(entity=None):
  if not entity:
    turnoff_media(entity=CLUSTER_ENTITIES_MEDIA)
  if isinstance(entity, list):
    for item in entity:
      turn_off(entity=item)

def turnoff_lights(entity=None, away=False):
  if not entity:
    turnoff_lights(entity=CLUSTER_ENTITIES_LIGHT)
  if isinstance(entity, str):
    if not away: 
      scene.air_control_turn_off(entity_id=entity)
    else:
      scene.air_control_turn_off(entity, transition=OFF_AWAY_TRANSITION)
  if isinstance(entity, list):
    for item in entity[:-1]:
      turn_off(entity=item)
    if away:
      task.air_control_sleep(transition)
    turn_off(entity[-1])
      
def turnoff_switches(entity=None):
  if not entity:
    turnoff_switches(entity=CLUSTER_ENTITIES_SWITCHES)
  if isinstance(entity, list):
    for item in entity:
      turn_off(entity=item)
      
def turnoff_tv(entity=None):
  if not entity:
    turnoff_tv(entity=CLUSTER_ENTITIES_TV)
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
  homeassistant.air_control_turn_off(entity_id=entity)
