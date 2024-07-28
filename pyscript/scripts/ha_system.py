import os
import sys
from collections import defaultdict
from homeassistant.const import EVENT_HOMEASSISTANT_STARTED
from constants.config import CFG_EVENT_STARTED_DELAY, CFG_LOG_SETTINGS_ENVIRONMEMT_LENGTH, CFG_PATH_DIR_PY, CFG_SYSTEM_ENVIRONMENT, CFG_SYSTEM_FILES, CFG_SYSTEM_LINKS
from constants.mappings import MAP_EVENT_SETUP_STARTED, MAP_EVENT_SYSTEM_STARTED
from utils import *

trigger = []

# Startup

@pyscript_executor
def event_setup_init_native(delay=CFG_EVENT_STARTED_DELAY):
  os.environ['PYTHONDONTWRITEBYTECODE'] = "1"
  sys.path.extend([
    path for path in [os.path.join(CFG_PATH_DIR_PY, subdir) for subdir in os.listdir(CFG_PATH_DIR_PY) if os.path.isdir(os.path.join(CFG_PATH_DIR_PY, subdir))]
    if path not in sys.path ])

@time_trigger
@event_trigger(EVENT_HOMEASSISTANT_STARTED)
def event_setup_init(delay=CFG_EVENT_STARTED_DELAY):
  event_setup_init_native()
  os.environ['PYTHONDONTWRITEBYTECODE'] = "1"
  sys.path.extend([
    path for path in [os.path.join(CFG_PATH_DIR_PY, subdir) for subdir in os.listdir(CFG_PATH_DIR_PY) if os.path.isdir(os.path.join(CFG_PATH_DIR_PY, subdir))]
    if path not in sys.path ])
    
  task.sleep(delay)
  event.fire(MAP_EVENT_SETUP_STARTED)

# Setup

@event_trigger(MAP_EVENT_SETUP_STARTED)
@logged
@service
def ha_setup():
  environment, paths, links = ha_setup_environment(), ha_setup_files(), ha_setup_links()
  event.fire(MAP_EVENT_SYSTEM_STARTED)
  return "\n".join([paths, links, environment])

# Tasks

def ha_setup_environment(variables=CFG_SYSTEM_ENVIRONMENT):
  def shorten(val, max_len=CFG_LOG_SETTINGS_ENVIRONMEMT_LENGTH):
    return val if len(val) <= max_len else val[:max_len] + '..'
  
  os.environ.update({k: v for k, v in variables.items() if not (k.startswith('S6') or k.startswith('__'))})
  env_vars = [f"{k}={shorten(os.environ[k])}" for k in sorted(os.environ.keys()) if not (k.startswith('S6') or k.startswith('__'))]
  
  formatted_env_vars = ", ".join(env_vars)
  return f"Environment:\n  {formatted_env_vars}"


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

  formatted_paths = "\n  ".join(formatted_paths)
  return f"System Path:\n  {formatted_paths}"

def ha_setup_links(links=CFG_SYSTEM_LINKS):
  for src, dest in links.items():
    if not os.path.isdir(dest) and os.path.islink(dest):
      os.unlink(dest)
    os.symlink(src, dest)
  formatted_links = "\n".join([f"{src} <- {dest}" for src, dest in links.items()])
  return f"Sym. Links:\n{formatted_links}"
