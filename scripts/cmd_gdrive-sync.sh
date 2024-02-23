#!/bin/bash

# Paths
VENV_DIR="./.venv"
SCRIPT_NAME="/config/scripts/script_gdrive-sync.py"

# Create virtual environment if not exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv $VENV_DIR
fi

# Activate virtual environment
source $VENV_DIR/bin/activate

# Install required Python modules
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client tqdm

# Run Python script concurrently
python $SCRIPT_NAME &

# Deactivate virtual environment
deactivate