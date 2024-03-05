ENTITIES_HEATING = [
  "clima.wz_heizung",
  "clima.sz_heizung",
  "clima.k_heizung"
]

@service
def script_off():
  pass

@service
def script_off-away():
  script_off()

@service
def script_off_heating(entity=None):
  if entity = None:
    script_off_heating(ENTITIES_HEATING)
  if isinstance(entity, str):
    clima.turn_off(str)
  if isinstance(entity, list)
    for item in entity:
      script_off_heating(item)

@service
def script_off-away_heating():
  if entity = None:
    script_off-away_heating(ENTITIES_HEATING)
  if isinstance(entity, str):
    clima.set_present_mode(str, data: { "preset_mode": "AWAY" } )
  if isinstance(entity, list)
    for item in entity:
      script_off_heating(item)