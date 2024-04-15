STATE_ON = "on"

# utils

FUNC_PYLOG = "pyscript.log"
FUNC_SYSLOG = "system_log.write"

# script_air_cleaner

SCRIPT_AIR_CLEANER_ENTITY = "fan.luftreiniger"
SCRIPT_AIR_CLEANER_ENTITY_ATTRIBUTE = "percentage"
SCRIPT_AIR_CLEANER_ENTITY_MODE = "mode"
SCRIPT_AIR_CLEANER_HELPER = ["switch.sz_luftung", "fan.wz_ventilator", "fan.sz_ventilator"]
SCRIPT_AIR_CLEANER_SENSOR = "sensor.luftreiniger"
SCRIPT_AIR_CLEANER_SENSOR_SPEED = "sensor.luftreiniger_geschwindigkeit"
SCRIPT_AIR_CLEANER_SPEED_THRESHOLD = 30
SCRIPT_AIR_CLEANER_PRESET_MODE_MANUAL = "manual"
SCRIPT_AIR_CLEANER_PRESET_MODE_SLEEP = "sleep"