# States

STATE_ON = "on"
STATE_OFF = "off"

STATE_HA_NONE = "None"
STATE_HA_UNAVAILABLE = "unavailable"
STATE_HA_UNKNOWN = "unknown"
STATES_HA_UNDEFINED = [STATE_HA_NONE, STATE_HA_UNAVAILABLE, STATE_HA_UNKNOWN]

STATE_HA_TIMER_STOPPED = "idle"

# Notifications

NOTIFICATION_ID_CHANGE_DETECTION = "changedetection"

# Shortcuts

SHORTCUT_HOUSING_NAME = "Notification-Monitor"

# Services

SERVICE_HA_TURN_OFF = "homeassistant.turn_off"
SERVICE_HA_SYSLOG_WRITE = "system_log.write"

SERVICE_PY_LOG = "pyscript.log"

# Scripts

SCRIPT_AIR_CLEANER_GROUP = "fan.luft"
SCRIPT_AIR_CLEANER_ENTITIES = [ "fan.wz_luft", "fan.sz_luft" ]
SCRIPT_AIR_CLEANER_ENTITY_ATTRIBUTE = "percentage"
SCRIPT_AIR_CLEANER_ENTITY_MODE = "mode"
SCRIPT_AIR_CLEANER_HELPER = ["switch.wz_luftung", "switch.sz_luftung"]
SCRIPT_AIR_CLEANER_SENSOR = [ "sensor.wz_luft", "sensor.sz_luft" ]
SCRIPT_AIR_CLEANER_SPEED_THRESHOLD = 30
SCRIPT_AIR_CLEANER_PRESET_MODE_MANUAL = "manual"
SCRIPT_AIR_CLEANER_PRESET_MODE_SLEEP = "sleep"