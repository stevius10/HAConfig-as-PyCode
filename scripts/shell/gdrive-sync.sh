#!/bin/bash

# Paths
VENV_DIR="/homeassistant/pyscript/environment/gdrive-sync"
SCRIPT_NAME="/homeassistant/pyscript/modules/gdrive-sync.py"

# Create virtual environment if not exists
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv $VENV_DIR > /dev/null
fi

# Activate virtual environment
source $VENV_DIR/bin/activate

# Install required Python modules
pip install google-auth google-auth-oauthlib google-api-core googleapis-common-protos google-auth-httplib2 google-api-python-client oauth2client httplib2 loguru tqdm > /dev/null

# Run Python script concurrently
python $SCRIPT_NAME 

# Deactivate virtual environment
deactivate