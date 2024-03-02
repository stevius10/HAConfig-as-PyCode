from constants import GIT_REPO_URL, GIT_BRANCH_NAME, GIT_COMMIT_MESSAGE, GIT_CREDENTIALS_PATH, GIT_CREDENTIALS_KEY, GIT_CREDENTIALS_CONFIG, SERVICE_CRON_GIT, PATH_LOGS

import subprocess
import logging
import os

def init(logfile=f"{PATH_LOGS}{os.path.basename(os.getcwd())}.log"): 
  with open(logfile, "w") as log:
    log.write("")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(logfile) 
        ]
    )
@service
def service_git_sync(repo_url=GIT_REPO_URL, branch_name=GIT_BRANCH_NAME, credentials_path=GIT_CREDENTIALS_PATH, key_path=GIT_CREDENTIALS_KEY,config_path=GIT_CREDENTIALS_CONFIG, commit_message=GIT_COMMIT_MESSAGE):
    try:
        subprocess.run(f"git config --local include.path '$(config_path)'", shell=True, check=True)

        subprocess.run(f"eval $(ssh-agent); ssh-add {key_path}", shell=True, check=True)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        subprocess.run(["git", "push", "origin", branch_name], check=True)

        merge_request_command = ["git", "push", "-o", "merge_request.create", "-o", "merge_request.target=develop"]
        subprocess.run(merge_request_command, check=True)

    except subprocess.CalledProcessError as e:
        logging.error(f"Error: {e}")