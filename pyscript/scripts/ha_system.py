from config import *
from utils import *

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
  if PYSCRIPT_DIR_NATIVE not in sys.path:
    sys.path.append(PYSCRIPT_DIR_NATIVE)

@event_trigger(EVENT_SYSTEM_STARTED)
def ha_setup_links(links=SYSTEM_LINKS):
  for source, target in links.items():
    if not os.path.exists(target):
      os.symlink(source, target)
<<<<<<< Updated upstream

@event_trigger(EVENT_SYSTEM_STARTED)
def ha_log_automations():
  pass
      
# Events

@event_trigger(EVENT_HOMEASSISTANT_STARTED)
def event_system_started(delay=EVENT_SYSTEM_STARTED_DELAY): 
=======
      
# Events

@time_trigger
def event_system_started(delay=SYSTEM_STARTED_EVENT_DELAY): 
>>>>>>> Stashed changes
  task.sleep(delay)
  event.fire(EVENT_SYSTEM_STARTED)
  log(EVENT_SYSTEM_STARTED)

@event_trigger(EVENT_CALL_SERVICE, "domain == 'pyscript' and service == 'reload'")
@event_trigger("SERVICE_RELOAD")
def on_pyscript_reload(**kwargs):
  log("on_pyscript_reload {kwargs}")