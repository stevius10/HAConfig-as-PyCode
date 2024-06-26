from constants.expressions import EXPR_TIME_SERVICE_FILEBACKUP_CRON
from constants.secrets import DEVICES, SYSTEM_FILES

DEVICES = {
  "home": [{"id": entry["id"], "default": entry["default"]} for entry in DEVICES["home"]],
  "mobile": [{"id": entry["id"], "default": entry["default"]} for entry in DEVICES["mobile"]]
}

DEFAULT_NOTIFICATION_TARGET = "home"

# Log

LOG_HA_FILE = "home-assistant.log"
LOG_HA_SIZE = 22
LOG_HA_SIZE_TAIL = 7

LOG_ARCHIVE_SIZE = LOG_HA_SIZE * 10
LOG_ARCHIVE_SUFFIX = "1"

LOG_TRUNCATE_BLOCK_DELAY = 5
LOG_TRUNCATE_IO_RETRY = 3

LOG_LOGGER_SYS = "py"
LOG_LOGGING_LEVEL = "info"

# Paths

PATH_DIR_CONFIG = "/config"
PATH_DIR_HOMEASSISTANT = "/homeassistant"

PATH_DIR_FILES = f"{PATH_DIR_CONFIG}/files"
PATH_DIR_STORAGE = f"{PATH_DIR_CONFIG}/.storage"

PATH_DIR_PY_LOG = f"{PATH_DIR_CONFIG}/pyscript/logs"
PATH_DIR_PY_NATIVE = f"{PATH_DIR_CONFIG}/pyscript/python"

PATH_LOG_HA = f"{PATH_DIR_CONFIG}/{LOG_HA_FILE}"
PATH_LOG_PY_HA = f"{PATH_DIR_PY_LOG}/{LOG_HA_FILE}"

PATH_DOCKER_LOG_HA = f"{PATH_DIR_HOMEASSISTANT}/{LOG_HA_FILE}"

# Services

SERVICE_AIR_CONTROL_ENABLED = False
SERVICE_GIT_SYNC_ENABLED = True
SERVICE_SCRAPE_HOUSING_ENABLED = True

SERVICES_AUTO = { 'shell_command.filebackup': EXPR_TIME_SERVICE_FILEBACKUP_CRON }

SERVICE_SCRAPE_HOUSING_BLACKLIST_DETAILS = ["WBS erforderlich", "mit WBS"]

# System

SYSTEM_CONFIG_EVENT_STARTED_DELAY = 3

# Setup 

SYSTEM_ENVIRONMENT = { 
  "ZDOTDIR": f"{PATH_DIR_STORAGE}/zsh" 
}

SYSTEM_FILES.update({ 
  f"{PATH_DIR_FILES}/.zshrc": f"{SYSTEM_ENVIRONMENT['ZDOTDIR']}/.zshrc"
})

SYSTEM_LINKS = { 
  PATH_DOCKER_LOG_HA: PATH_LOG_PY_HA, 
  f"{PATH_DOCKER_LOG_HA}.{LOG_ARCHIVE_SUFFIX}": f"{PATH_LOG_PY_HA}.{LOG_ARCHIVE_SUFFIX}"
}