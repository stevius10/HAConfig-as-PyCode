# System
SYSTEM_FILES = {
    "/config/.storage/id_rsa": "/root/.ssh", 
}

# Services
SERVICE_GOOGLE_DRIVE_LOCAL_FOLDER ="/share/Extern"
SERVICE_GOOGLE_DRIVE_REMOTE_FOLDER ="1-vl3qWDz5Fm8QtiQFBx-4uuwRO7dHls1"
SERVICE_GOOGLE_DRIVE_TRASH_FOLDER ="19q7mSrN0iFBhicZ6PESPgshyRFeuAQpe"
SERVICE_GOOGLE_DRIVE_IGNORE_FOLDERS = '[".Spotlight-V100", "Downloads", "Sicherungen"]'
SERVICE_GOOGLE_DRIVE_CREDENTIALS_FILE = "/config/.storage/google/google_auth.json"

SERVICE_GIT_REPO_URL="git@github.com/stevius10/home-assistant-config.git"
SERVICE_GIT_REPO_BRANCH="feature/ha-config-changes"
SERVICE_GIT_REPO_TARGET="develop"
SERVICE_GIT_REPO_MESSAGE="auto/sync"
SERVICE_GIT_SETTINGS_CREDENTIALS = "/config/.storage/git/id_rsa"
SERVICE_GIT_SETTINGS_CONFIG="/config/.storage/git/.gitconfig"