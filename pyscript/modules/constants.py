import datetime

# General

DAYTIME =  "cron(* 9-19 * * 1-6)"

# System
SYSTEM_FILES = {
    "/config/.storage/id_rsa": "/root/.ssh", 
    "/config/files/.zshrc": "/root", 
  }

# Time
TIME_DATE_RANGE_AIR_CLEANER = "range('02/01 20:00', '10/01 20:00')"

# Path
PATH_CONSTANTS = "/config/pyscript/modules/constants.py"
PATH_LOG_HA = "/config/home-assistant.log"
PATH_LOGS = "/config/logs/"

# Log
LOG_HA_SIZE = 80
LOG_HA_ARCHIVE_SIZE = 10 * LOG_HA_SIZE
LOG_ARCHIVE_SUFFIX = "1"
LOG_DEBUG_DEVICES = ["fan.luftreiniger"]

# Automation
AUTO_CONFIG_MOTION_SUNSET_DIFF = 30
AUTO_CONFIG_MOTION_TRANSITION = 20
AUTO_CONFIG_MOTION_TIMEOUT = 60

AUTO_CONFIG_OFF_AWAY_TRANSITION = 90

AUTO_CONFIG_TIMER_DURATION_LUFTREINIGER = 5400
AUTO_CONFIG_TIMER_DURATION_SZ_VENTILATOR = 5400
AUTO_CONFIG_TIMER_DURATION_SCHLAFZIMMER = 5400

# Scripts
SCRIPT_AIR_CLEANER_THRESHOLD = 10

# Services
SERVICE_GOOGLE_DRIVE_CRON = "cron(15 1 * * *)"
SERVICE_GOOGLE_DRIVE_LOCAL_FOLDER ="/share/Extern"
SERVICE_GOOGLE_DRIVE_REMOTE_FOLDER ="1-vl3qWDz5Fm8QtiQFBx-4uuwRO7dHls1"
SERVICE_GOOGLE_DRIVE_TRASH_FOLDER ="19q7mSrN0iFBhicZ6PESPgshyRFeuAQpe"
SERVICE_GOOGLE_DRIVE_IGNORE_FOLDERS = '[".Spotlight-V100", "Downloads", "Sicherungen"]'
SERVICE_GOOGLE_DRIVE_CREDENTIALS_FILE = "/config/.storage/google/google_auth.json"

SERVICE_GIT_CRON = "cron(0 1 * * *)"
SERVICE_GIT_REPO_URL="git@github.com/stevius10/home-assistant-config.git"
SERVICE_GIT_REPO_BRANCH="feature/ha-config-changes"
SERVICE_GIT_REPO_TARGET="develop"
SERVICE_GIT_REPO_MESSAGE="auto/sync"
SERVICE_GIT_SETTINGS_CREDENTIALS = "/config/.storage/git/id_rsa"
SERVICE_GIT_SETTINGS_CONFIG="/config/.storage/git/.gitconfig"

# Events
EVENT_FOLDER_WATCHER = "folder_watcher"
EVENT_SYSTEM_PYSCRIPT_RELOADED = "event_system_pyscript_reloaded"
# EVENT_SYSTEM_LOG_TRUNCATED = "event_system_log_truncated"

# States
STATE_HA_NONE = "None"
STATE_HA_UNAVAILABLE = "unavailable"
STATE_HA_UNKNOWN = "unknown"
STATES_HA_UNDEFINED = [STATE_HA_NONE, STATE_HA_UNAVAILABLE, STATE_HA_UNKNOWN]
# STATE_HA_TIMER_STOPPED = "idle"