from constants import GIT_REPO_URL, GIT_BRANCH_NAME, GIT_BRANCH_TARGET, GIT_COMMIT_MESSAGE, GIT_CREDENTIALS_KEY, GIT_CREDENTIALS_CONFIG, SERVICE_CRON_GIT
from log import Log

import datetime
import subprocess

@service
@time_trigger(SERVICE_CRON_GIT)
def service_git_sync(repo_url=GIT_REPO_URL, branch_name=GIT_BRANCH_NAME, branch_target=GIT_BRANCH_TARGET, key_path=GIT_CREDENTIALS_KEY, config_path=GIT_CREDENTIALS_CONFIG, commit_message=GIT_COMMIT_MESSAGE):
  
  util = Log(pyscript.get_global_ctx())
  
  commands = [
    f"git config --local include.path '{config_path}'",
    f"eval $(ssh-agent); ssh-add {key_path}", 
    f"git add .",
    f"git commit -m '{commit_message}'", 
    f"git push origin {branch_name}", 
    f"git push -o merge_request.create -o merge_request.target={branch_target}"
  ]
  
  for command in commands: 
    try:
      result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, check=False, text=True)
      util.log([command, result.stdout, result.stderr])
    except subprocess.CalledProcessError as e:
      util.log([e, command, result.stdout, result.stderr])

  return util.finished()