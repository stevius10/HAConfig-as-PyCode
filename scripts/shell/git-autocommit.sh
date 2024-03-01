#!/bin/bash

apk add  git # git-credential-store

REPO_URL=${1:-$REPO_URL}
BRANCH_NAME=${2:-$BRANCH_NAME}
GIT_CREDENTIALS_PATH=${3:-$GIT_CREDENTIALS_PATH}
GIT_CONFIG_PATH=${4:-$GIT_CONFIG_PATH}
GIT_COMMIT_MESSAGE=${5:-$GIT_COMMIT_MESSAGE}


cd /config

git config --global user.name "Steven Koch"
git config --global user.email steven.johann.koch@googlemail.com
git config core.sshCommand "ssh -i /homeassistant/.storage/git/git-ssh -F /dev/null"

git push --set-upstream origin feature/ha-config-changes
if [[ $(git status --porcelain) ]]; then
    
    git checkout -b $BRANCH_NAME
    
    git add .
    git commit -m "$GIT_COMMIT_MESSAGE"
    
    git push origin $BRANCH_NAME
    
fi