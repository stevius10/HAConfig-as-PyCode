from config import (
    SERVICE_GIT_CRON, SERVICE_GIT_REPO_URL,
    SERVICE_GIT_REPO_BRANCH, SERVICE_GIT_REPO_TARGET,
    SERVICE_GIT_REPO_MESSAGE, SERVICE_GIT_SETTINGS_CREDENTIALS,
    SERVICE_GIT_SETTINGS_CONFIG
)
from utils import Logfile
import subprocess

@service(supports_response="optional")
@time_trigger(SERVICE_GIT_CRON)
def service_git_sync(
  repo_url=SERVICE_GIT_REPO_URL,
  branch_name=SERVICE_GIT_REPO_BRANCH,
  branch_target=SERVICE_GIT_REPO_TARGET,
  key_path=SERVICE_GIT_SETTINGS_CREDENTIALS,
  config_path=SERVICE_GIT_SETTINGS_CONFIG,
  commit_message=SERVICE_GIT_REPO_MESSAGE
):
  logfile = Logfile(pyscript.get_global_ctx())
  pyscript.log(msg="test")
  commands = [
      f"git config --local include.path '{config_path}'",
      f"eval $(ssh-agent); ssh-add {key_path}", 
      
      # read on system
      f"cd /config",
      f"git checkout {branch_name}",
      f"git pull origin {branch_name}",
      f"git add .",
      f"git commit -m '{commit_message}'", 
      f"git push origin {branch_name}",
      
      # write on copy
      #f"rm -rf /share/home-assistant-config; cd /share",
      #f"git clone {repo_url}; cd /share/home-assistant-config",
      #f"git pull origin {branch_target}; git checkout origin {branch_name}",
      #f"git merge {branch_target}; git push -u origin {SERVICE_GIT_REPO_BRANCH}"
  ]

  for command in commands:
      try:
          result = subprocess.run(
              command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
              shell=True, check=False, text=True
          )
          logfile([command, result.stdout, result.stderr])
      except subprocess.CalledProcessError as e:
          logfile([e, command, result.stdout, result.stderr])

  return logfile.finished()