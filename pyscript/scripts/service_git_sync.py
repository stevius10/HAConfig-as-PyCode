from constants import GIT_REPO_URL, GIT_BRANCH_NAME, GIT_COMMIT_MESSAGE, GIT_CREDENTIALS_PATH, GIT_CREDENTIALS_KEY, GIT_CREDENTIALS_CONFIG, SERVICE_CRON_GIT, PATH_LOGS
from log import Log

import subprocess

@service
def service_git_sync(repo_url=GIT_REPO_URL, branch_name=GIT_BRANCH_NAME, credentials_path=GIT_CREDENTIALS_PATH, key_path=GIT_CREDENTIALS_KEY,config_path=GIT_CREDENTIALS_CONFIG, commit_message=GIT_COMMIT_MESSAGE):
    log = Log(pyscript.get_global_ctx())
    try:
        log.log("test")
        config_output = subprocess.run(f"git config --local include.path '{config_path}'", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        log.log(config_output.stdout)
        log.log(config_output.stderr)

        ssh_output = subprocess.run(f"eval $(ssh-agent); ssh-add {key_path}", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        log.log(ssh_output.stdout)
        log.log(ssh_output.stderr)

        add_output = subprocess.run(["git", "add", "."], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        log.log(add_output.stdout)
        log.log(add_output.stderr)

        commit_output = subprocess.run(["git", "commit", "-m", commit_message], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        log.log(commit_output.stdout)
        log.log(commit_output.stderr)

        # subprocess.run(["git", "push", "origin", branch_name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # merge_request_command = ["git", "push", "-o", "merge_request.create", "-o", "merge_request.target=develop"]
        # subprocess.run(merge_request_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    except subprocess.CalledProcessError as e:
        log(f"Error: {e}")