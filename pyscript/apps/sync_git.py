import subprocess

from constants.config import CFG_SERVICE_ENABLED_SYNC_GIT
from constants.expressions import *
from constants.secrets import *
from utils import *


@service(supports_response="optional")
@time_trigger(EXPR_TIME_SYNC_GIT)
@state_active(str(CFG_SERVICE_ENABLED_SYNC_GIT))
@logged
def sync_git(
  key_path=SEC_SERVICE_GIT_SETTINGS_CREDENTIALS,
  config_path=SEC_SERVICE_GIT_SETTINGS_CONFIG,
  branch = SEC_SERVICE_GIT_REPO_BRANCH,
  message = SEC_SERVICE_GIT_REPO_MESSAGE
):
  return dict(sync(pyscript.get_global_ctx(), config_path, key_path, branch, message))
 
@pyscript_executor
def sync(name, config_path, key_path, branch, message):
  
  from logfile import Logfile # req. sys setup 
  logfile = Logfile(name)
  
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