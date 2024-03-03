AUTO_CONFIG_DEFAULT_RESET_DELAY = 180
AUTO_CONFIG_MOTION_SUNSET_DIFF = 30
AUTO_CONFIG_MOTION_TRANSITION = 20
AUTO_CONFIG_MOTION_TIMEOUT = 60

EVENT_FOLDER_WATCHER = "folder_watcher"

GOOGLE_DRIVE_LOCAL_FOLDER ="/share/Extern"
GOOGLE_DRIVE_FOLDER_ID ="1-vl3qWDz5Fm8QtiQFBx-4uuwRO7dHls1"
GOOGLE_DRIVE_TRASH_FOLDER_ID ="19q7mSrN0iFBhicZ6PESPgshyRFeuAQpe"
GOOGLE_DRIVE_CREDENTIALS_FILE = "/config/.storage/google/google_auth.json"

# GIT_CREDENTIALS_PATH="/config/.storage/git/git-credentials"
GIT_CREDENTIALS_KEY = "/config/.storage/git/id_rsa"
GIT_CREDENTIALS_CONFIG="/config/.storage/git/.gitconfig"

GIT_REPO_URL="git@github.com/stevius10/home-assistant-config.git"
GIT_BRANCH_NAME="feature/ha-config-changes"
GIT_BRANCH_TARGET="develop"
GIT_COMMIT_MESSAGE="auto commit"

HA_PATH_LOG = "/config/home-assistant.log"
HA_PATH_LOG_ARCHIVE = "/config/home-assistant.archive.log"

HA_STATE_NONE = "None"
HA_STATE_UNAVAILABLE = "unavailable"
HA_STATE_UNKNOWN = "unknown"

HA_STATES_UNDEFINED = [HA_STATE_NONE, HA_STATE_UNAVAILABLE, HA_STATE_UNKNOWN]

PATH_CONSTANTS = "/config/pyscript/modules/constants.py"
PATH_LOGS = "/config/logs/"

SERVICE_CRON_GIT = "cron(0 5 * * *)"

SIZE_LOG_ENTRIES = 25
SIZE_LOG_ARCHIVE_ENTRIES = 75