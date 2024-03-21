from config import SYSTEM_FILES

from homeassistant.const import EVENT_HOMEASSISTANT_STARTED

import shutil
import os

@event_trigger(EVENT_HOMEASSISTANT_STARTED)
def ha_setup_files(file=SYSTEM_FILES):
  try:
    for file in files:
      shutil.copy2(file, files[file])
  except Exception as e:
    log.warn(e)
