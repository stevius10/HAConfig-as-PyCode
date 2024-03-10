from constants import SERVICE_GIT_CRON, SERVICE_GIT_REPO_URL, \
SERVICE_GIT_REPO_BRANCH, SERVICE_GIT_REPO_TARGET, SERVICE_GIT_REPO_MESSAGE, \
SERVICE_GIT_SETTINGS_CREDENTIALS, SERVICE_GIT_SETTINGS_CONFIG
from logfile import Logfile
import subprocess

@service
@time_trigger(SERVICE_GIT_CRON)
def service_git_sync(repo_url=SERVICE_GIT_REPO_URL, branch_name=SERVICE_GIT_REPO_BRANCH, branch_target=SERVICE_GIT_REPO_TARGET, key_path=SERVICE_GIT_SETTINGS_CREDENTIALS, config_path=SERVICE_GIT_SETTINGS_CONFIG, commit_message=SERVICE_GIT_REPO_MESSAGE):
  
  logfile = Logfile(pyscript.get_global_ctx())
  
  commands = [
    f"git config --local include.path '{config_path}'",
    f"eval $(ssh-agent); ssh-add {key_path}", 
    f"git add .",
    f"git commit -m '{commit_message}'", 
    f"git push origin {branch_name}"
  ]
  
  for command in commands: 
    try:
      result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, check=False, text=True)
      logfile.log([command, result.stdout, result.stderr])
    except subprocess.CalledProcessError as e:
      logfile.log([e, command, result.stdout, result.stderr])

  return logfile.finished()