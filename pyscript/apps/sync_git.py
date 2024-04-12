from config import (
    SERVICE_GIT_CRON, secrets
)
from utils import Logfile
import subprocess
import aiohttp
import asyncio

logfile = Logfile(pyscript.get_global_ctx())

async def create_or_update_pull_request(repo_owner, repo_name, base_branch, head_branch, title, body):
    access_token = secrets.SERVICE_GIT_GITHUB_TOKEN
    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls"
    payload = {
        "title": title,
        "body": body,
        "base": base_branch,
        "head": head_branch
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status == 201:
                return await response.json(), None
            elif response.status == 422:
                pull_request_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{head_branch}"
                async with session.patch(pull_request_url, json=payload, headers=headers) as response:
                    if response.status == 200:
                        return await response.json(), None
            return None, f"Failed to create or update pull request: {response.status}"

@service(supports_response="optional")
@time_trigger(SERVICE_GIT_CRON)
def service_git_sync(
  repo_url=secrets.SERVICE_GIT_REPO_URL,
  repo_owner=secrets.SERVICE_GIT_GITHUB_USER,
  repo_name=secrets.SERVICE_GIT_REPO_NAME,
  base_branch=secrets.SERVICE_GIT_REPO_BASE,
  branch_name=secrets.SERVICE_GIT_REPO_BRANCH,
  branch_target=secrets.SERVICE_GIT_REPO_TARGET,
  key_path=secrets.SERVICE_GIT_SETTINGS_CREDENTIALS,
  config_path=secrets.SERVICE_GIT_SETTINGS_CONFIG,
  commit_message=secrets.SERVICE_GIT_REPO_MESSAGE,
  pull_request_title=secrets.SERVICE_GIT_GITHUB_PR_TITLE,
  pull_request_body=secrets.SERVICE_GIT_GITHUB_PR_BODY
):
  
  commands = [
      f"git config --local include.path '{config_path}'",
      f"eval $(ssh-agent); ssh-add {key_path}", 
      
      # Stash local changes
      "git stash",
      
      # Pull from main branch
      "git checkout main",
      "git pull origin main",
      
      # Switch back to the working branch
      f"git checkout {branch_name}",
      
      # Merge changes from main branch
      "git merge main",
      
      # Apply stashed changes
      "git stash pop",
      
      # Push changes to the working branch
      "git add .",
      f"git commit -m '{commit_message}'", 
      f"git push origin {branch_name}",
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

  # Create or update pull request
  loop = asyncio.get_event_loop()
  response, error = loop.run_until_complete(create_or_update_pull_request(repo_owner, repo_name, base_branch, branch_name, pull_request_title, pull_request_body))
  if response:
      logfile.log(f"Pull request created or updated: {response['html_url']}")
  else:
      logfile.log(f"Error: {error}")

  return logfile.finished()