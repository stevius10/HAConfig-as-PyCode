# States

from homeassistant.const import STATE_ON, STATE_OFF, STATE_UNAVAILABLE, STATE_UNKNOWN

STATES_UNDEFINED = [STATE_UNAVAILABLE, STATE_UNKNOWN]

STATE_HA_TIMER_STOPPED = "idle"

# Notifications

NOTIFICATION_ID_CHANGE_DETECTION = "changedetection"

# Shortcuts

SHORTCUT_HOUSING_NAME = "SC-HA-Notify-Housing"
SHORTCUT_HOUSING_PARAMETER_URL = "url"

# Services

SERVICE_HA_TURN_OFF = "homeassistant.turn_off"
SERVICE_HA_SYSLOG_WRITE = "system_log.write"

SERVICE_PY_LOG = "pyscript.log"

# Scripts

SCRIPT_AIR_CLEANER_ENTITY_ATTRIBUTE = "percentage"
SCRIPT_AIR_CLEANER_ENTITY_MODE = "mode"
SCRIPT_AIR_CLEANER_PRESET_MODE_MANUAL = "manual"
SCRIPT_AIR_CLEANER_PRESET_MODE_SLEEP = "sleep"