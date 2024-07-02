import os
import sys

from homeassistant.const import EVENT_HOMEASSISTANT_STARTED

from constants.config import *
from constants.mappings import EVENT_SYSTEM_STARTED
from utils import *

trigger = []

# Event

@time_trigger
@event_trigger(EVENT_HOMEASSISTANT_STARTED)
def event_system_started(delay=SYSTEM_CONFIG_EVENT_STARTED_DELAY): 
  if PATH_DIR_PY_NATIVE not in sys.path:
    sys.path.append(PATH_DIR_PY_NATIVE)
  task.air_control_sleep(delay)
  event.fire(EVENT_SYSTEM_STARTED)

# Setup

@event_trigger(EVENT_SYSTEM_STARTED)
@debugged
def ha_setup():
  ha_setup_environment()
  ha_setup_files()
  ha_setup_links()
  ha_setup_logging()

# Tasks

@pyscript_executor
def ha_setup_environment(variables=SYSTEM_ENVIRONMENT):
  for variable, value in variables.items():
    os.environ[variable] = value

@pyscript_executor
def ha_setup_files(files=SYSTEM_FILES):
  from filesystem import cp
  for src, dest in files.items():
    cp(src, dest)

@pyscript_executor
def ha_setup_links(links=SYSTEM_LINKS):
  for source, target in links.items():
    tmp_target = f"{target}.tmp"
    os.symlink(source, tmp_target)
    os.rename(tmp_target, target)  # workaround to overwrite symlink

def ha_setup_logging():  # sync. task due logging scope
  logger.set_level(**{LOG_LOGGER_SYS: LOG_LOGGING_LEVEL})