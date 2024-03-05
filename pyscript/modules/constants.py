AUTO_CONFIG_DEFAULT_RESET_DELAY = 600
AUTO_CONFIG_MOTION_SUNSET_DIFF = 30
AUTO_CONFIG_MOTION_TRANSITION = 20
AUTO_CONFIG_MOTION_TIMEOUT = 60

EVENT_FOLDER_WATCHER = "folder_watcher"

GOOGLE_DRIVE_LOCAL_FOLDER ="/share/Extern"
GOOGLE_DRIVE_REMOTE_FOLDER ="1-vl3qWDz5Fm8QtiQFBx-4uuwRO7dHls1"
GOOGLE_DRIVE_TRASH_FOLDER ="19q7mSrN0iFBhicZ6PESPgshyRFeuAQpe"
GOOGLE_DRIVE_IGNORE_FOLDERS = '[".Spotlight-V100", "Downloads", "Sicherungen"]'
GOOGLE_DRIVE_CREDENTIALS_FILE = "/config/.storage/google/google_auth.json"

GIT_CREDENTIALS_KEY = "/config/.storage/git/id_rsa"
GIT_CREDENTIALS_CONFIG="/config/.storage/git/.gitconfig"

GIT_REPO_URL="git@github.com/stevius10/home-assistant-config.git"
GIT_BRANCH_NAME="feature/ha-config-changes"
GIT_BRANCH_TARGET="develop"
GIT_COMMIT_MESSAGE="auto/sync"


HA_STATE_NONE = "None"
HA_STATE_UNAVAILABLE = "unavailable"
HA_STATE_UNKNOWN = "unknown"

HA_STATES_UNDEFINED = [HA_STATE_NONE, HA_STATE_UNAVAILABLE, HA_STATE_UNKNOWN]

PATH_CONSTANTS = "/config/pyscript/modules/constants.py"
PATH_LOGS = "/config/logs/"
PATH_LOG_HA = "/config/home-assistant.log"

SERVICE_CRON_GIT = "cron(0 2 * * *)"
SERVICE_CRON_GOOGLE_DRIVE = "cron(0 3 * * *)"

SIZE_LOG_ENTRIES = 2000
SIZE_LOG_ARCHIVE_ENTRIES = 10000