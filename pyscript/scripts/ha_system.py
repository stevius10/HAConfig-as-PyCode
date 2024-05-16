from config import *
from utils import *

from events import EVENT_SYSTEM_STARTED

from homeassistant.const import EVENT_HOMEASSISTANT_STARTED, EVENT_CALL_SERVICE

import datetime
import logging
import regex as re
import shutil
import os

# Automations 

@event_trigger(EVENT_SYSTEM_STARTED)
def ha_setup_files(files=SYSTEM_FILES):
  for file in files:
    shutil.copy2(file, files[file])
    
@event_trigger(EVENT_SYSTEM_STARTED)
def ha_setup_logging():
  logger.set_level(**{LOG_LOGGER_SYS: LOG_LOGGING_LEVEL})

@event_trigger(EVENT_SYSTEM_STARTED)
def ha_setup_environment():
  if PATH_DIR_PY_NATIVE not in sys.path:
    sys.path.append(PATH_DIR_PY_NATIVE)

@event_trigger(EVENT_SYSTEM_STARTED)
@service
def ha_setup_links(links=SYSTEM_LINKS):
  for source, target in links.items():
    tmp_target = f"{target}.tmp"
    # shortcut to overwrite symlink
    os.symlink(source, tmp_target)
    os.rename(tmp_target, target)

# Events

@time_trigger
@event_trigger(EVENT_HOMEASSISTANT_STARTED)
def event_system_started(delay=SYSTEM_STARTED_EVENT_DELAY): 
  task.sleep(delay)
  event.fire(EVENT_SYSTEM_STARTED)