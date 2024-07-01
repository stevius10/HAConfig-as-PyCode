from constants.config import SERVICE_GIT_SYNC_ENABLED
from constants.expressions import *
from constants.secrets import *
from constants.settings import *

import subprocess
import requests

from utils import *

@service(supports_response="optional")
@time_trigger(EXPR_TIME_SERVICE_GIT_CRON)
@state_active(str(SERVICE_GIT_SYNC_ENABLED))
@logged
def service_git_sync(
  key_path=SERVICE_GIT_SETTINGS_CREDENTIALS, 
  config_path=SERVICE_GIT_SETTINGS_CONFIG,
  branch = SERVICE_GIT_REPO_BRANCH, 
  message = SERVICE_GIT_REPO_MESSAGE
):
  return dict(git_sync(pyscript.get_global_ctx(), config_path, key_path, branch, message))
 
@pyscript_executor
def git_sync(name, config_path, key_path, branch, message):
  
  from logfile import Logfile # req. sys setup 
  logfile = Logfile(ctx=name)
  
  commands  = [
      f"git config --local include.path '{config_path}'", f"eval $(ssh-agent); ssh-add {key_path}", 
      "git stash", f"git pull origin {branch}", f"git checkout {branch}", "git stash apply",
      "git add .", f"git commit -m '{message}'", f"git push origin {branch}"
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
  
  return logfile.close()