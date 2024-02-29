import subprocess
import logging
import os
from constants import GIT_SSH_KEY_PATH, GIT_SYNC_CRON, GIT_REPO_URL, GIT_BRANCH_NAME, GIT_CREDENTIALS_PATH, GIT_CONFIG_PATH, GIT_COMMIT_MESSAGE, GIT_CMD_FILE, PATH_LOGS
from pathlib import Path

NAME = "auto_git"
logging.basicConfig(filename=f"{PATH_LOGS}{NAME}.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def git_commit(**kwargs):
    try:
        command = f"eval $(ssh-agent); ssh-add {GIT_SSH_KEY_PATH}"
        subprocess.run(command, shell=True, check=True)
        
        subprocess.run([
            "bash",
            GIT_CMD_FILE,
            GIT_REPO_URL,
            GIT_BRANCH_NAME,
            GIT_CREDENTIALS_PATH,
            GIT_CONFIG_PATH, 
            GIT_COMMIT_MESSAGE
        ], check=True)
        
    except subprocess.CalledProcessError as e:
        logging.error(f"{e}")

git_commit()