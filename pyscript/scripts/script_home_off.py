CONFIG_AWAY_TRANSITION = 90

ENTITIES_AIR = [
  "humidifier.luftbefeuchter", 
  "fan.luftreiniger",
  "fan.sz_ventilator",
  "switch.sz_lufter"
]

ENTITIES_HEATING = [
  "clima.wz_heizung",
  "clima.sz_heizung",
  "clima.k_heizung"
]

ENTITIES_MEDIA= [
  "media_player.bad"
  "media_player.kueche"
  "media_player.schlafzimmer"
  "media_player.wohnzimmer"
  "media_player.uberall"
]

ENTITIES_SCENES = [
  "scene.wz_aus",
  "scene.sz_aus",
  "scene.g_aus",
  "scene.k_aus"
]

ENTITIES_SCRIPTS = [
  "script.gh_luften"
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
  script_off_media()
  script_off_scenes(away=away)
  script_off_scripts()
  script_off_switches()
  script_off_tv()
  
@service
def script_off_away():
  script_off(away=True)

@service
def script_off_air(entity=None, reset=True):
  if entity == None:
    script_off_air(entity=ENTITIES_AIR)
  if isinstance(entity, str):
    fan.turn_off(entity)
    humidifier.turn_off(entity)
    switch.turn_off(entity)
  if isinstance(entity, list):
    for item in entity:
      script_off_air(entity=item)

@service
def script_off_heating(entity=None, away=False):
  if entity == None:
    script_off_heating(entity=ENTITIES_HEATING, away=away)
  if isinstance(entity, str):
    if not away: 
      clima.turn_off(entity)
    else:
      clima.set_present_mode(str, preset_mode="AWAY")
  if isinstance(entity, list):
    for item in entity:
      script_off_heating(entity=item, away=away)

@service
def script_off_media(entity=None):
  if entity == None:
    script_off_media(entity=ENTITIES_MEDIA)
  if isinstance(entity, str):
    media_player.turn_off(entity)
  if isinstance(entity, list):
    for item in entity:
      script_off_media(entity=item)

@service
def script_off_scenes(entity=None, away=False):
  if entity == None:
    script_off_scenes(entity=ENTITIES_SCENES)
  if isinstance(entity, str):
    if not away: 
      script.turn_on(entity)
    else:
      scene.turn_on(entity, transition=CONFIG_AWAY_TRANSITION)
  if isinstance(entity, list):
    for item in entity:
      script_off_scenes(entity=item)

@service
def script_off_scripts(entity=None):
  if entity == None:
    script_off_scripts(entity=ENTITIES_SCRIPTS)
  if isinstance(entity, str):
    script.turn_off(entity)
  if isinstance(entity, list):
    for item in entity:
      script_off_scripts(entity=item)

@service
def script_off_switches(entity=None):
  if entity == None:
    script_off_switches(entity=ENTITIES_SWITCHES)
  if isinstance(entity, str):
    switch.turn_off(entity)
  if isinstance(entity, list):
    for item in entity:
      script_off_switches(entity=item)
      
@service
def script_off_tv(entity=None):
  if entity == None:
    script_off_tv(entity=ENTITIES_TV)
  if isinstance(entity, str):
    try: 
      androidtv.adb_command(entity_id=entity)
    except Exception: 
      webostv.command(entity_id=entity)
  if isinstance(entity, list):
    for item in entity:
      script_off_tv(entity=item)
      
# Helper

@service
def turn_off(entity="light.wz_lampe_1"):
  light.turn_on(entity)
  log.info(state.get(entity, domain))
  light.turn_off(entity)
