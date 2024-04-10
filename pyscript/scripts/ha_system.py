from config import PATH_LOGS, PYSCRIPT_DIR_NATIVE, SYSTEM_FILES

from homeassistant.const import EVENT_HOMEASSISTANT_STARTED

import datetime
import logging
import inspect
import regex as re
import shutil
import os

@event_trigger(EVENT_HOMEASSISTANT_STARTED)
def ha_setup_files(file=SYSTEM_FILES):
  try:
    for file in files:
      shutil.copy2(file, files[file])
  except Exception as e:
    log.warn(e)

@event_trigger(EVENT_HOMEASSISTANT_STARTED)
def ha_setup_environment():
  if PYSCRIPT_DIR_NATIVE not in sys.path:
    sys.path.append(PYSCRIPT_DIR_NATIVE)