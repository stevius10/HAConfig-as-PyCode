import os
import sys

from collections import defaultdict
from pathlib import Path

from homeassistant.const import EVENT_HOMEASSISTANT_STARTED

from constants.config import * 
from constants.mappings import MAP_EVENT_SETUP_STARTED, MAP_EVENT_SYSTEM_STARTED, MAP_RESULT_STATUS

from utils import *

trigger = []

# Startup

@pyscript_executor # native written redundancy intended
def event_setup_init_native(delay=CFG_EVENT_STARTED_DELAY):
  os.environ['PYTHONDONTWRITEBYTECODE'] = "1"
  sys.path.extend([path for path in [os.path.join(CFG_PATH_DIR_PY, subdir) for subdir in os.listdir(CFG_PATH_DIR_PY) if os.path.isdir(os.path.join(CFG_PATH_DIR_PY, subdir))] if path not in sys.path ])

@time_trigger
@event_trigger(EVENT_HOMEASSISTANT_STARTED)
def event_setup_init(delay=CFG_EVENT_STARTED_DELAY):
  event_setup_init_native()
  os.environ['PYTHONDONTWRITEBYTECODE'] = "1"
  sys.path.extend([path for path in [os.path.join(CFG_PATH_DIR_PY, subdir) for subdir in os.listdir(CFG_PATH_DIR_PY) if os.path.isdir(os.path.join(CFG_PATH_DIR_PY, subdir))] if path not in sys.path ])

  task.sleep(delay)
  event.fire(MAP_EVENT_SETUP_STARTED)

@event_trigger(MAP_EVENT_SETUP_STARTED)
@service
def ha_setup():
  result = { **ha_setup_environment(), **ha_setup_files(),  **ha_setup_logging(), **ha_setup_links() }
  event.fire(MAP_EVENT_SYSTEM_STARTED)
  return result 

# Setup

@logged
def ha_setup_environment(variables=CFG_SYSTEM_ENVIRONMENT):
  def shorten(val, max_len=CFG_LOG_SETTINGS_ENVIRONMEMT_LENGTH):
    return val if len(val) <= max_len else val[:max_len] + '..'

  os.environ.update({k: v for k, v in variables.items() if not (k.startswith('S6') or k.startswith('__'))})
  env_vars = [f"{k}={shorten(os.environ[k])}" for k in sorted(os.environ.keys()) if not (k.startswith('S6') or k.startswith('__'))]
  return resulted(status=MAP_RESULT_STATUS.SUCCEED, entity=ha_setup_environment.get_name(), message=", ".join(env_vars))

@logged
def ha_setup_files(files=CFG_SYSTEM_FILES):
  from filesystem import cp
  for src, dest in files.items():
    cp(src, dest)
  
  paths = defaultdict(list)
  seen_keys = set()

  for path in sys.path:
    if path.startswith('__'):
      continue
    split_path = path.split(os.sep)
    if len(split_path) > 4:
      key = os.sep.join(split_path[:4])
      path = key + "/..."
      seen_keys.add(key)
    else:
      key = os.sep.join(split_path[:3]) if len(split_path) > 3 else path
    paths[key].append(path)
  
  formatted_paths = []
  for key in sorted(paths.keys()):
    if key in seen_keys:
      formatted_paths.append(f"{key}/…")
    else:
      formatted_paths.append(", ".join(paths[key]))
  return resulted(status=MAP_RESULT_STATUS.SUCCEED, entity=ha_setup_files.get_name(), message="\n  ".join(formatted_paths))

@logged
def ha_setup_links(links=CFG_SYSTEM_LINKS):
  for src, dest in links.items():
    if not os.path.isdir(dest) and os.path.islink(dest):
      os.unlink(dest)
    os.symlink(src, dest)
  formatted_links = "\n".join([f"{src} <- {dest}" for src, dest in links.items()])
  return resulted(status=MAP_RESULT_STATUS.SUCCEED, entity=ha_setup_links.get_name(), message=formatted_links)

@logged
def ha_setup_logging():  # sync. task due logging scope
  logger.set_level(**{CFG_LOG_LOGGER: CFG_LOG_LEVEL})
  return resulted(status=MAP_RESULT_STATUS.SUCCEED, entity=ha_setup_logging.get_name(), message=Path(CFG_PATH_DIR_LOG, f"{CFG_LOGFILE_DEBUG_FILE}.log"))
