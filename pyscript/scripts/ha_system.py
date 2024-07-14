import os
import sys
from homeassistant.const import EVENT_HOMEASSISTANT_STARTED

from constants.config import CFG_PATH_DIR_PY, CFG_EVENT_STARTED_DELAY, CFG_SYSTEM_ENVIRONMENT, CFG_SYSTEM_FILES, CFG_SYSTEM_LINKS
from constants.mappings import MAP_EVENT_SETUP_STARTED, MAP_EVENT_SYSTEM_STARTED

from utils import *

trigger = []

# Initialization

# @pyscript_executor # code redundancy suppress to pass code runtime wise
# def ha_setup_init_native(path=CFG_PATH_DIR_PY):
#   os.environ['PYTHONDONTWRITEBYTECODE'] = "1"
#   sys.path.extend([path for path in [os.path.join(CFG_PATH_DIR_PY, subdir) for subdir in os.listdir(CFG_PATH_DIR_PY) if os.path.isdir(os.path.join(CFG_PATH_DIR_PY, subdir))] if path not in sys.path])
#   return [path for path in sys.path]

@time_trigger
@event_trigger(EVENT_HOMEASSISTANT_STARTED)
@logged
def event_setup_init(delay=CFG_EVENT_STARTED_DELAY):
  os.environ['PYTHONDONTWRITEBYTECODE'] = "1"
  sys.path.extend([path for path in [os.path.join(CFG_PATH_DIR_PY, subdir) for subdir in os.listdir(CFG_PATH_DIR_PY) if os.path.isdir(os.path.join(CFG_PATH_DIR_PY, subdir))] if path not in sys.path])
  # ha_setup_init_native()
  
  task.sleep(delay)
  event.fire(MAP_EVENT_SETUP_STARTED)
  
  return [path for path in sys.path]

# Setup

@event_trigger(MAP_EVENT_SETUP_STARTED)
@logged
@service
def ha_setup():
  results = ha_setup_environment(), ha_setup_files(), ha_setup_links()
  event.fire(MAP_EVENT_SYSTEM_STARTED)
  return results

# Tasks
  
# @pyscript_executor
def ha_setup_environment(variables=CFG_SYSTEM_ENVIRONMENT):
  for variable, value in variables.items():
    os.environ[variable] = value
  return [f"{key}: {value}" for key, value in os.environ.items()]

@pyscript_executor
def ha_setup_files(files=CFG_SYSTEM_FILES):
  from filesystem import cp
  for src, dest in files.items():
    cp(src, dest)
  return [path for path in sys.path]

@pyscript_executor
def ha_setup_links(links=CFG_SYSTEM_LINKS):
  for source, target in links.items():
    if not os.path.isdir(target) and os.path.islink(target):
      os.unlink(target)
    os.symlink(source, target)
  return [f"{source} <- {target}" for source, target in links.items()]
