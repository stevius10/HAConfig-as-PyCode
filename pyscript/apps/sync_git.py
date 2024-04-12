from config import (
  SERVICE_GIT_CRON, SERVICE_GIT_REPO_URL, SERVICE_GIT_REPO_NAME, 
  SERVICE_GIT_GITHUB_USER, SERVICE_GIT_GITHUB_TOKEN,
  SERVICE_GIT_SETTINGS_CREDENTIALS,   SERVICE_GIT_REPO_MAIN, 
  SERVICE_GIT_REPO_BRANCH, SERVICE_GIT_REPO_TARGET, 
  SERVICE_GIT_REPO_MESSAGE, SERVICE_GIT_GITHUB_PR_TITLE, 
  SERVICE_GIT_GITHUB_PR_BODY, SERVICE_GIT_SETTINGS_CONFIG
)
from utils import Logfile

import dump
import subprocess
import requests

logfile  = Logfile(pyscript.get_global_ctx())

def create_or_update_pull_request(repo_owner, repo_name, base_branch, head_branch, title, body):
    access_token  =  SERVICE_GIT_GITHUB_TOKEN
    headers  = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    url  = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls"
    payload  = {
        "title": title,
        "body": body,
        "base": base_branch,
        "head": head_branch
    }
    response  = await task.executor(requests.get, url, json=payload, headers=headers)
    #logfile.log(f"{response['status_code']}: {response['json']}")
    if response.status_code == 201:
        return response.json()["html_url"]
    elif response.status_code == 422:
        pull_request_url  = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{head_branch}"
        response  = requests.patch(pull_request_url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()["html_url"]
    return None

@service(supports_response="optional")
@time_trigger(SERVICE_GIT_CRON)
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
  
  commands  = [
      f"git config --local include.path '{config_path}'",
      f"eval $(ssh-agent); ssh-add {key_path}", 
      "git stash",
      
      "git checkout main",
      "git pull origin main",
      f"git checkout {branch_name}",
      "git merge main",
      
      "git stash pop",
      "git add .",
      f"git commit -m '{commit_message}'", 
      f"git push origin {branch_name}",
  ]

  for command in commands:
    try:
      result  = subprocess.run(
          command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
          shell=True, check=False, text=True
      )
      logfile.log([command, result.stdout, result.stderr])
    except subprocess.CalledProcessError as e:
      logfile.log([e, command, result.stdout, result.stderr])

  pull_request_url  = create_or_update_pull_request(repo_owner, repo_name, base_branch, branch_name, pull_request_title, pull_request_body)
  if pull_request_url:
      logfile.log(f"Pull request created or updated: {pull_request_url}")
  else:
      logfile.log("Failed to create or update pull request.")

  return logfile.finished()