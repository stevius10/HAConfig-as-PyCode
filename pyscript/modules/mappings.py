# States

STATE_ON = "on"
STATE_OFF = "off"

# Scripts

SCRIPT_AIR_CLEANER_GROUP = "fan.luft"
SCRIPT_AIR_CLEANER_ENTITIES = [ "fan.wz_luft", "fan.sz_luft" ]
SCRIPT_AIR_CLEANER_ENTITY_ATTRIBUTE = "percentage"
SCRIPT_AIR_CLEANER_ENTITY_MODE = "mode"
SCRIPT_AIR_CLEANER_HELPER = ["switch.sz_luftung", "switch.wz_ventilator"]
SCRIPT_AIR_CLEANER_SENSOR = [ "sensor.wz_luft", "sensor.sz_luft" ]
SCRIPT_AIR_CLEANER_SPEED_THRESHOLD = 30
SCRIPT_AIR_CLEANER_PRESET_MODE_MANUAL = "manual"
SCRIPT_AIR_CLEANER_PRESET_MODE_SLEEP = "sleep"

# Helper

FUNC_PYLOG = "pyscript.log"
FUNC_SYSLOG = "system_log.write"