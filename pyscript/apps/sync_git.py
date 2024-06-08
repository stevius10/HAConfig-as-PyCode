from constants.expressions import *
from constants.secrets import *
from constants.settings import *

import subprocess
import requests

@service(supports_response="optional")
@time_trigger(EXPR_TIME_SERVICE_GIT_CRON)
def service_git_sync(
  repo_url = SERVICE_GIT_REPO_URL,
  repo_owner = SERVICE_GIT_GITHUB_USER,
  repo_name = SERVICE_GIT_REPO_NAME,
  base_branch = SERVICE_GIT_REPO_MAIN,
  branch_name = SERVICE_GIT_REPO_BRANCH,
  branch_target = SERVICE_GIT_REPO_TARGET,
  key_path = SERVICE_GIT_SETTINGS_CREDENTIALS,
  config_path = SERVICE_GIT_SETTINGS_CONFIG,
  commit_message = SERVICE_GIT_REPO_MESSAGE,
  pull_request_title = SERVICE_GIT_GITHUB_PR_TITLE,
  pull_request_body = SERVICE_GIT_GITHUB_PR_BODY
):
  
  from logfile import Logfile # runtime level due sys path config
  logfile  = Logfile(pyscript.get_global_ctx())
  
  commands  = [
      f"git config --local include.path '{config_path}'",
      f"eval $(ssh-agent); ssh-add {key_path}", 
      
      "git stash",
      f"git pull origin {branch_name}",
      f"git checkout {branch_name}",
      "git stash apply",
      
      "git add .",
      f"git commit -m '{commit_message}'", 
      f"git push origin {branch_name}"
  ]

  for command in commands:
    try:
      result = subprocess.run(
          command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
          shell=True, check=False, text=True
      )
      logfile.log([command, result.stdout, result.stderr])
    except subprocess.CalledProcessError as e:
      logfile.log([e, command, result.stdout, result.stderr])

  # return logfile.close()